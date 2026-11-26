/* Telegram Mini App adapter, shared by every page in this site.
   Include right after telegram-web-app.js:
     <script src="https://telegram.org/js/telegram-web-app.js"></script>
     <script src="../tg.js"></script>
   Optional per-page settings on <html>:
     data-tg-header="#1240e0"   colour of Telegram's top bar
     data-tg-bg-light / data-tg-bg-dark   page background, so there's no flash at the edges
   Outside Telegram (a normal browser) this file does nothing. */
(function () {
  var tg = window.Telegram && window.Telegram.WebApp;
  if (!tg || !tg.initData) return;

  var root = document.documentElement;
  var ds = root.dataset;

  tg.ready();   // hides Telegram's loading placeholder
  tg.expand();  // full height instead of half sheet

  // Long pages scroll up and down; without this a downward swipe at the top
  // collapses the whole Mini App instead of scrolling (Bot API 7.7+).
  if (tg.isVersionAtLeast && tg.isVersionAtLeast('7.7')) tg.disableVerticalSwipes();

  function paint() {
    var dark = tg.colorScheme === 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    if (!tg.isVersionAtLeast || !tg.isVersionAtLeast('6.1')) return;
    var bg = dark ? ds.tgBgDark : ds.tgBgLight;
    if (bg) tg.setBackgroundColor(bg);
    if (ds.tgHeader) tg.setHeaderColor(ds.tgHeader);
    else if (bg) tg.setHeaderColor(bg);
    if (bg && tg.isVersionAtLeast('7.10')) tg.setBottomBarColor(bg);
  }
  paint();
  tg.onEvent('themeChanged', paint);

  // In fullscreen mode (link with &mode=fullscreen) Telegram draws its buttons
  // over the page, so push content below them.
  function safe() { root.classList.toggle('tg-fs', !!tg.isFullscreen); }
  safe();
  tg.onEvent('fullscreenChanged', safe);
  var st = document.createElement('style');
  st.textContent =
    'html.tg-fs body{padding-top:calc(var(--tg-safe-area-inset-top,0px) + var(--tg-content-safe-area-inset-top,0px))}' +
    'html.tg-fs [data-tg-sticky]{top:calc(var(--tg-safe-area-inset-top,0px) + var(--tg-content-safe-area-inset-top,0px))!important}';
  document.head.appendChild(st);
})();

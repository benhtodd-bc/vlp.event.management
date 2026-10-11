// Serves the generated event tracker (index.html). Rebuild with ../build_tracker.py --site, then clasp push.
function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Clearwater Oct 2026 - event tracker')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL); // lets a Google Site embed it
}

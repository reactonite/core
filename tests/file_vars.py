minimal_working_example = """<head>Test header</head>
<body>
<h1>Heading</h1>
<p>Parargraph</p>
<a href="https://google.com">Link</a>
</body>
"""

minimal_working_example_js = """
        import React from 'react';
        import Helmet from 'react-helmet';
        

        function App() {return (<><Helmet>
 Test header
</Helmet>
<h1>Heading</h1><p>Parargraph</p><a href="https://google.com">Link</a></>);}

        export default App;
        """

full_working_example = """<!doctype html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="./static/main.css">
  <title>Reactonite App</title>

</head>

<body>
  <div class="main">
    <header class="main-header">
      <img src="./static/logo.png" class="logo" alt="Reactonite" />
      <p>
        Entry point is <code>src/index.html</code>, save to auto reload.
      </p>
      <a class="link" href="https://github.com/SDOS2020/Team_3_Reactonite/" target="_blank" rel="noopener noreferrer">
        Learn about Reactonite
      </a>
    </header>
  </div>
  <script src="./static/main.js"></script>
</body>

</html>
"""

full_working_example_js = """
        import React from 'react';
        import Helmet from 'react-helmet';
        

        function App() {return (<><Helmet>
 <meta charSet="utf-8"/>
 <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport"/>
 <link rel="stylesheet" src="./static/main.css"/>
 <title>
  Reactonite App
 </title>
</Helmet>
<div className="main">
<header className="main-header">
<img alt="Reactonite" className="logo" src="./static/logo.png"/>
<p>
        Entry point is <code>src/index.html</code>, save to auto reload.
      </p>
<a className="link" href="https://github.com/SDOS2020/Team_3_Reactonite/" rel="noopener noreferrer" target="_blank">
        Learn about Reactonite
      </a>
</header>
</div><script src="./static/main.js"></script></>);}

        export default App;
        """

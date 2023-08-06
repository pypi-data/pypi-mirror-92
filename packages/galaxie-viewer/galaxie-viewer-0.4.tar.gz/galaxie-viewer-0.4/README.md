[![pipeline status](https://gitlab.com/Tuuux/galaxie-viewer/badges/master/pipeline.svg)](https://gitlab.com/Tuuux/galaxie-viewer/commits/master) [![coverage report](https://gitlab.com/Tuuux/galaxie-viewer/badges/master/coverage.svg)](https://gitlab.com/Tuuux/galaxie-viewer/commits/master) [![Documentation Status](https://readthedocs.org/projects/glxviewer/badge/?version=latest)](https://glxviewer.readthedocs.io/en/latest/?badge=latest)

Galaxie Viewer
==============
A small terminal viewer, use by Galaxie Tools for display something to the terminal.
<div style="text-align:center"><img src ="https://gitlab.com/Tuuux/galaxie-viewer/raw/master/docs/source/images/logo_galaxie.png" /></div>

The Mission
-----------
Provide a Text Based line viewer, it use a template.
It existe many template for high level language, but nothing for text one.

Our mission is to provide useful display template for terminal. Actually every Galaxie tool use it; where print() is not use any more...

Screenshots
-----------
v0.2
<p align="center">
<img src="https://gitlab.com/Tuuux/galaxie-viewer/raw/master/docs/source/images/screen_01.png">
</p>

Example
-------

```python
import sys
import time
from GLXViewer import viewer


def main():
    start_time = time.time()
    viewer.flush_infos(
        column_1=__file__,
        column_2='Yes that is possible'
    )
    viewer.flush_infos(
        column_1=__file__,
        column_2='it have no difficulty to make it',
        column_3='what ?'
    )
    viewer.flush_infos(
        column_1='Use you keyboard with Ctrl + c for stop the demo',
        status_text='INFO',
        status_text_color='YELLOW',
        status_symbol='!',
    )
    while True:

        viewer.flush_infos(
            column_1=__file__,
            column_2=str(time.time() - start_time),
            status_text='REC',
            status_text_color='RED',
            status_symbol='<',
            prompt=True
        )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        viewer.flush_a_new_line()
        sys.exit()
```
Documentations
--------------
Readthedocs link: https://glxviewer.readthedocs.io

Installation
------------
For PyPI (last stable) version:
```bash
pip install galaxie-viewer
```

For TestPyPI (last) version
```bash
pip install -i https://test.pypi.org/simple/ galaxie-viewer
```
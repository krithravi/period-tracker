# Period Tracker

Here's a period tracker built with Python.
It's totally open source, and your data can just live on _your_ machine
as opposed to someone else's server.

## How to use it
You should probably first clone the repo.
After installing the necessary dependencies (probably `pandas`, `dash`, and `numpy`),
run `python app.py <filename>`.
This data file should contain all the data you want as a CSV.
I've left a testing dataset called `data.csv` as a starter!

Head over to (probably) `http://127.0.0.1:8050` where you'll see the app served!
After  that, you'll get something like the following (based off the `data.csv` testing data):
![Sample demo](sample.png)

## Future
More features coming soon! I'm looking to have a GUI way to supply/modify files
(I'm guessing people won't want to edit a CSV every time).
I'm also guessing people might want to track other symptoms, so I'll try to find a way
to incorporate/visualize those as well! If you have any other ideas or tips, feel free
to add an issue! I'll also try to make it a bit prettier - it's a bit _too_ bare-bones right now.

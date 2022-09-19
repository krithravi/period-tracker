# Period Tracker

Here's a period tracker built with Python.
It's totally open source, and your data can just live on _your_ machine
as opposed to someone else's server.
This app doesn't ping the internet _at all_ - not even to get
the fonts.
The prediction portions are totally transparent! You won't have to wonder
how the algorithm magically comes up with a predicted date.

## How to use it
You should probably first clone the repo.
After installing the necessary dependencies (probably `pandas`, `dash`, and `numpy`),
run `python app.py <filename>`.
This data file should contain all the data you want as a CSV.
I've left a testing dataset called `data.csv` as a starter!

Head over to (probably) `http://127.0.0.1:8050` where you'll see the app served!
After that, you'll get something like the following (based off the `data.csv` testing data):

![Sample demo](sample.png)

## How it works
- Average and standard deviation are used as the measures of center and spread respectively
- The start date of next cycle is computed as the date of the last cycle plus average length of cycle (outliers removed)
- The end date of the next cycle is computed as the predicted start date plus the average length of the period (outliers removed)
- The "likely to start as early as" prediction uses the predicted start date minus one standard deviation of the cycle length (outliers removed) in days
- Outliers are detected using the 1.5 IQR rule
- The fertile window is computed as starting 14 days before the start of the next predicted cycle and as lasting for 5 days. These parameters can be modified between the "START USER MODIFICATION" and "END USER MODIFICATION" sections in `app.py`. Whether information regarding the fertile window is displayed can be toggled in the same section.

## Future
More features coming soon!
- I really want the calendar to have the relevant dates highlighted.
- I'm looking to have a GUI way to supply/modify files (I'm guessing people won't want to edit a CSV every time).
- I'm also guessing people might want to track other symptoms, so I'll try to find a way to incorporate/visualize those as well!
- If you have any other ideas or tips, feel free to add an issue!

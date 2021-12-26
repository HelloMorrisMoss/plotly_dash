# speeds_study_nh

This project was a production speed study looking at the trends over time of different products on several production lines. It was placed on hold due to production fluctuations from the Covid-19 pandemic and its many effects.

This study used productioncondition history collected with Ignition processed through several steps. First within Ignition the tag history was tabularized to be easily aggregated using a daily gateway timer script. The data is then loaded into pandas dataframes for on-demand visualization using a Plotly-Dash/Bootstrap front-end.

## Example Graphs

There were hundreds of graphs made during development and many more possible using the Dash/Bootstrap controls, these are few examples. The product has been intentionally blurred.

This graph shows the ratio of the product on that production line that was produced at different proportions of the target speed from 0.70 to 1.30 weekly over several months. The size of the circles represent the quantity produced during the week.

![A line chart with many colorful lines showing the trends of production speeds over several months.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/speed_study_nh/target_by_week.png)

These charts show the percentage and length of the product that was produced at speeds close to the target speed.
* The first shows a part that the target speed was as intended challenging but achievable.
* In second the target was too low and the operators regularly exceeded it. About half the length shown here. The target for parts like these could be increased.
* For the third the target was clearly too high for the current process and was identified as a prime candidate for productivity improvements.
![A line graph showing a mostly horizontal line with an intense increase as it approaches a vertical red target line, almost asymptotically.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/speed_study_nh/on%20target.png)

![A line graph showing a bumpy horizontal line with an intense increase after crossing a vertical red target line, peaking and comming down before ending.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/speed_study_nh/target%20low.png)

![A line graph showing a mostly horizontal line with a singular peak and ending a significant distance short of a vertical red target line.](https://github.com/HelloMorrisMoss/diagrams_and_images/blob/main/speed_study_nh/all%20low%20coater-tcode%20graph.png)

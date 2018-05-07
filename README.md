

# Title: 
Monte Carlo Project Cost Estimator


## Team Member(s):
Suyash Singh

# Monte Carlo Simulation Scenario & Purpose:

The purpose of this simulation predicts the cost of completion of a project. The University Startup IT company hires graduate students with skill sets to work within 3 of the following teams.

1. Design
2. Development
3. Testing

These student's hourly wage depends on their skillset and their total wage would depend on the number of hours they have worked on that particular task.

The Monte Carlo Project Cost Estimator could be used in two scenarios.

### Case 1

When the company works similar project where the timeline for the completion of these tasks does not vary a great deal and the company has enough historical data that would estimate the time taken for the completion of each task. In this scenario the company would load/update the average time required for the task. In this case, the hypothetical times for the completion of the tasks are considered as:

- Design - 14 hours 
- Development - 10 hours 
- Testing - 6 hours.

And the overhead cost is considered as 5% to 40% of the Fixed Cost
 
 ### Case 2
 
The company works on a variety of project where the time taken to complete these tasks varies to a greater extent. In this case, the tool will ask the client to enter an estimated time and allowable overhead time associated with that task.
 
## Simulation's variables of uncertainty

1. Fixed Cost for the completion of the project
    - Beta-PERT Distribution  
2. Total overhead cost associated with the project (Resources, Interviewing cost, Training, Certification)
    - Beta-Pert Distribution

Here, I did research on the to UIUC hourly wages regulations for graduate assistants, they are paid within the range of $8.25 (minimum) - $18.00 (maximum) per hour. And hourly wages of students working on such technical tasks is usually on the higher side, hence the "most likely" value for PERT distribution is considered as $14.4 per hour.

I feel this is a good representation of reality.

On the other hand, the overhead time required to complete the project was considered to be 5% (minimum) to 40% (maximum) of the fixed time for that task and the most likely is taken to be 32%.

The overhead time could really vary given that only graduate students are hired. Their availability can vary depending on various factors like exams, availability of resources, training cost for new employees, any extra certification required, interviewing cost). I feel the variability, in this case, is very difficult to predict without having any historical data.

## Hypothesis or hypotheses before running the simulation:

1. In case 1, The time of completion of each task is as follows: i. Design - 14 hours ii. Development - 10 hours iii. Testing - 6 hours

2. The overhead cost would be a result of extra hours worked on a particular task. Which would range between 5% and 40%.

3. The min and max values of the salary given to the graduate assistant as per UIUC regulations vary from $8.25/hour to $18.00/hour depending on the position and skillset.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

## Instructions on how to use the program:

## All Sources Used:
1. https://www.riskamp.com/beta-pert
2. https://github.com/iSchool-590PR-2018Spring/in-class-examples/blob/master/week_12_Prob_Distributions.ipynb

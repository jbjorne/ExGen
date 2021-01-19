# Feature Vectors

A telemarketing company is calling potential customers from their database. The most likely new customers to call are predicted using the nearest neighbour algorithm, which is trained on customers already called (training set). Feature vectors are constructed using the categorical variables 1) gender (0=male, 1=female), 2) age (0 if under 50 else 1) 3), city (0=London, 1=other), 4) children (0=no, 1=yes) and 5) marital status (0=unmarried, 1=married). The 5-dimensional feature vector could thus be for example [00101](example). The class of a person is [1](example) if anything was sold to them and [-1](example) otherwise.

[persons]()

* Define the feature vectors for the persons dataset. Vector 1: [vec1](answer), 2: [vec2](answer), 3: [vec3](answer), 4: [vec4](answer), 5: [vec5](answer), 6: [vec6](answer).
* Calculate the Manhattan distances between the test set and the training set examples. Distance 1-5: [dist5-1](answer), 2-5: [dist5-2](answer), 3-5: [dist5-3](answer), 4-5: [dist5-4](answer), 1-6: [dist6-1](answer), 2-6: [dist6-2](answer), 3-6: [dist6-3](answer), 4-6: [dist6-4](answer).
* What class does the nearest neighbour method predict for the test set examples: Predicted class for example 5: [class5](answer) and for example 6: [class6](answer).


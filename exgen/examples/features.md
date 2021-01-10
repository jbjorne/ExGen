# Feature Vectors

Widget Inc. is using telemarketing to sell its new product in Finland. The company has acquired a large list of potential customers, and to speed up the sales process, people who are similar to the company's existing customers are called first. To find potential customers most like existing ones, the potential customers are classified using a nearest neighbours classifier.

The feature vector is constructed using the following categorical variables:

* gender (0=male, 1=female)
* age group (0 if under 30, otherwise 1)
* residence (0=rest of the country, 1=Helsinki)
* children (0=no, 1=yes)
* marital status (0=unmarried, 1=married)

The class of the example (0, 1 or 2) is defined so that if the customer has made at most 5 purchases, the class is 0, if at most 10 purchases the class is 1 and otherwise the class is 2.

[](persons)

Define the feature vectors for the persons dataset. A feature vector is defined as xxxxx, where each feature can be 0 or 1, for example [00101](example).

* Feature vector 1: [vec1](answer)
* Feature vector 2: [vec2](answer)
* Feature vector 3: [vec3](answer)
* Feature vector 4: [vec4](answer)
* Feature vector 5: [vec5](answer)
* Feature vector 6: [vec6](answer)

Calculate the Manhattan distances between the test set (persons 5 and 6) and the training set (persons 1-4):

* Distance 1-5: [dist5-1](answer)
* Distance 2-5: [dist5-2](answer)
* Distance 3-5: [dist5-3](answer)
* Distance 4-5: [dist5-4](answer)

* Distance 1-6: [dist6-1](answer)
* Distance 2-6: [dist6-2](answer)
* Distance 3-6: [dist6-3](answer)
* Distance 4-6: [dist6-4](answer)

Using the nearest neighbours method, predict the class for the test set examples:

* Predicted class for example 5: [class5](answer)
* Predicted class for example 6: [class6](answer)


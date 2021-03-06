SmartSweepers version Py                    |
========================                    |
Author: Yati Sagade                         |
                                            |
Inspiration: Mat Buckland(Fup)'s C++ code   |
             at http://www.ai-junkie.com    |
                                            |
Mail: yati dot sagade at gmail dot com      |
--------------------------------------------+


![screenshot](https://raw.githubusercontent.com/yati-sagade/SmartSweepers/master/smartsweepers.png)


This is my take on the classic example of the workings of an 
Artificial Neural Network, originally found at http://www.ai-junkie.com/
The original(Fup's) code was C++/Win32.

Well, if you don't know already, here's what we're trying to achieve:
Using ANNs and learning through the Genetic Algorithm(GA), breed a set of mine-
sweepers that wander around gobbling up any mines in the world. The total number
of mines in the world at any instant is constant - so when a mine is swept, 
another appears somewhere in the world. The fittest minesweepers are displayed
in a different colour (I prefer green for the fittest, and blue for the rest).

Running
=======
i)    Install Python 2.x if you haven't done so already.
ii)   On the shell, `cd` to this directory.
iii)  Make sure you have pygame installed. On the prompt, say
        
        $ pip install pygame

      Ofcourse, you'll need to have pip installed. For that,
        
        $ yum install pip

      or your system's equivalent pkg-mgmt command should do the job.
iv)  type
        
        $ python main.py
            
            OR

        $ ./main.py



For the graphical rendering, the fantastic pygame library has been used, and 
hence, of course, pygame is needed to run the program.


Lowdown on the files in this project:

genetic_algorithm.py
	The Genetic Algorithm module, should be pretty easy to understand provided
	you've been reading up on Fup's excellent tutorial on the topic.

neuralnet.py
	Home for the Neuron, NeuronLayer and NeuralNet classes.

minesweeper.py
	provides the Mine and MineSweeper classes.

geom2D.py
	This is the mathematical grit that goes behind all the fancy stuff :)
	It is home to the Matrix2D, Vector2D and PointList classes. PointList
	subclasses Matrix2D and is used to store the vertices of our sweepers and
	mines as a matrix of 2D points. We only needed multiplication of matrices
	for the basic transforms using normalized co-ordinates, so only 
	Matrix2D.__mul__() is implemented leaving aside __add__, __sub__ or __div__.
	
	If you don't know what normalized co-ordinates are, panic not. They're just
	a way to represent points such that transformations(like rotation, 
	translation, etc) are reduced to a chain of matrix multiplications.
	This requires the addition of an extra co-ordinate(yes, that's 3
	co-ordinates for 2D points). This extra co-ordinate is almost always chosen
	to be fixed at unity(1). So, (0,0) becomes (0,0,1) and (2.75,5) becomes 
	(2.75, 5, 1) and so on.
	
	The benefit is that by defining transformation matrices - one for
	rotation, one for translation, one for scaling and so on - that respect the
	normalized co-ordinates, we can effectively express every transformation as
	a matrix multiplication, thus allowing for chaining transforms. There's even
	an algorithm to find the most efficient order of multiplying matrices given 
	a matrix multiplication expression by exploiting associativity of matrix 
	multiplication.
	
settings.py
	Global settings - Equivalent of CParams.cpp and params.ini in Fup's code.

utils.py
	miscellaneous utility functions

controller.py
	The "duct tape" that glues together all other components of this project.
	it takes care of creating the minesweepers, breeding generations of them and
	rendering them.

main.py
	This just creates the pygame window, and loops throught the event loop while
	invoking a Controller instance's functions to update and render the world. 

resources/
	Currently contains the icon I ripped from Fup's code(that was originally in 
        .ico format, I made a GIF of it - hopefully not offending anyone).

TODO: 	(i) Any improvement in performance
	(ii) Make the code conform to PyLint conventions 
	    (currently the score is really bad!).


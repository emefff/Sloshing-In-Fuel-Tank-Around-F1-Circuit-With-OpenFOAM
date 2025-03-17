# Sloshing-Of-Fuel-In-Tank-Around-F1-Circuit-With-OpenFOAM
Based on one of the tutorials for sloshing fluids in tanks (namely sloshingTank3D6DoF) we can build a fairly accurate simulation of tank going round a Formula 1 circuit with actual F1 accelerations. 
What do we need for that? First of all, we need a tank for our fuel to slosh around in. Obviously, we do not have a .step file of a real F1 tank. If you have ever seen one, they are quite complicated.
For the purpose of our demo, any tank will do. On the GrabCAD homepage, we find a model of a purpose built fuel tank which looks a bit like a WRC tank (https://grabcad.com/library/fuel-tank-b1-1).
However, there have been many errors in this step, so a complete redesign and defeatureing was necessary. Find the result in the shared folder.
The simulation is quite simple in terms of patches, we only have one patch, which is the walls of the tank. The two baffles inside are also modeled in 3D, so we do not have to worry about 
a createBafflesDict. We just have mesh properly. 
What else is needed? We need to fill the tank via a setFieldsDict. In order to see the flow through the slots in the baffles, we chose a low amount of fuel.
The 6DoF example is very handy in that it only needs a file with points in space and time and rotation angles around the axes. Here's where the fun starts.
There is a Python library called 'fastf1'. It offers access to a database of Formula 1 data, we extract the fastest qualifying lap at the Austrian Grand Prix 2021. Verstappen's lap was approx. 63.72s,
we have access to positional data too. From this we calculate the Euler angles, and the position itself will do as displacement data if we subtract the first position (this gives us (0 0 0) as our first
position). Just to prove everything is correct, we can sum up the length of the vectors in our file, we get 4295.4396m, which is very close to the official track length of 4326m. The reason for the difference is,
due to the calculation we have to drop the last value.

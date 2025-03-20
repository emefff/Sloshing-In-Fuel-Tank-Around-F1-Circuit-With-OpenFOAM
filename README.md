# Sloshing-In-Fuel-Tank-Around-F1-Circuit-With-OpenFOAM
Based on one of the tutorials for sloshing fluids in tanks (namely sloshingTank3D6DoF) we can build a fairly accurate simulation of tank going round a Formula 1 circuit with actual F1 accelerations. 
What do we need for that? First of all, we need a tank for our fuel to slosh around in. Obviously, we do not have a .step file of a real F1 tank. If you have ever seen one, they are quite complicated.
For the purpose of our demo, any tank will do. On the GrabCAD homepage, we find a model of a purpose built fuel tank which looks a bit like a WRC tank (https://grabcad.com/library/fuel-tank-b1-1).
However, there have been many errors in this step, so a complete redesign and defeatureing was necessary. Find the result in the shared folder:

![Bildschirmfoto vom 2025-03-19 15-20-13](https://github.com/user-attachments/assets/bed649b6-c65f-4cc4-9a0e-5767e3426860)

The simulation is quite simple in terms of patches, we only have one patch, which is the walls of the tank. The two baffles inside are also modeled in 3D, so we do not have to worry about 
a createBafflesDict. We just have mesh properly. 
What else is needed? We need to fill the tank via a setFieldsDict. In order to see the flow through the slots in the baffles, we chose a low amount of fuel of approx. 50%.
The simulation is performed with a k-omega turbulent, multiphase (air and fuel) interFoam. 
The 6DoF example is very handy in that it only needs a file with points in space (displacement realtive to an origin) and time and Euler angles around the axes (in total per line (x, y, z), (roll, yaw, pitch) ). Here's where the fun starts:

There is a Python library called 'fastf1'. It offers access to a database of Formula 1 data, we extract the fastest qualifying lap at the Austrian Grand Prix 2021. Verstappen's lap was approx. 63.72s,
we have access to positional data too. From this we calculate the Euler angles, and the position itself will do as displacement data if we subtract the first position (this gives us (0 0 0) as our first
position right at start/finish). Just to prove everything is correct, we can sum up the length of the vectors in our file, we get 4295.4396m, which is very close to the official track length of 4326m. Due to the calculation we have to drop the last value.
We plot the GPS data and verify everything is indeed correct (the z-axis is grossly exaggerated compared to the other two). Do you notice Verstappen's slight wobble in the second corner? He could have had an even better qualifiying time:

![Bildschirmfoto vom 2025-03-19 14-34-45](https://github.com/user-attachments/assets/89c26e3a-03ce-4f6e-8352-2ec3a1892e5f)

It is important to distinguish between these data and the actual track layout. The data just represents one single lap of one car, and there are many ways and techniques to complete a lap very quickly. Running the Python program also allows for 
estimating the velocities from the data, and one of the problems is, that in between the first and second data point we get around 295km/h (right at start/finish of this qualifying lap). The initial state of the fuel in the tank is just 
created with a setFields (it represents a level at stand still), the tank is approx. half filled. This immediately sends the fuel splashing around, as for the simulation in the first timestep, this represents a very large artificial acceleration (the first deltaT don't matter either, they are always chosen to be very small). It is obvious right from the start, that such a simple fuel tank would not be usable in F1. In F1, tanks are rubber bladders filled with fire retardant foams to prevent this extreme sloshing and splashing. Otherwise, permanent 
disruptions of fuel supply would be the case. Additionally, they use 2-4 pumps in the corners of the tank, these feed into an intermediate reservoir where the first high pressure pump is located. This pump never runs out of fuel, no matter the acceleration of the car. 
Let's take a brief look at an alpha.fuel result:

![alpha_water_t0 15s](https://github.com/user-attachments/assets/87ce285b-8470-4715-8771-4cdefea8e58f)

So, what is the use of such a simulation? With it, we may gather information about 

-) where to place pump inlets

-) forces on the hull of the tank (here: quite substantial) 

-) amount of air/gas swirled into the fuel

-) is a fuel/gas separator needed (here: yes)

-) is a foam needed (here: yes)

-) where to put additional baffles (here: if no foam, additional baffles along both axis)

-) does the tank shape create any problems

-) how does the fuel surface look like under certain accelerations (braking!)

-) etc.

The video shared is a demo, as the full simulation of the whole circuit is still running. The translation of the fuel tank is not shown, only the rotation.

emefff@gmx.at


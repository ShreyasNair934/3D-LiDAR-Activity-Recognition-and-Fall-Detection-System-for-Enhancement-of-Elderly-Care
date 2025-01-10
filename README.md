# 3D LiDAR Activity Recognition and Fall Detection System for Enhancement of Elderly Care

## Abstract
The elderly population has been rapidly rising in the recent years, placing extra demand on
healthcare facilities like hospitals and aged care facilities. This rising demographic has also
placed a lot of pressure on healthcare professionals like doctors, nurses and carers due to a
critical shortage of staff. Therefore, round the clock monitoring of vulnerable elderly patients
susceptible to falls and gait disorders, proves to be immensely difficult. Often random falls of
elderly patients go unnoticed for many minutes or even hours. When the patient is discovered,
irreversible damage to their body and health would have already occurred. This paper proposes
a novel IoT-enabled LiDAR framework designed for real-time detection of anomalies in the
Activities of Daily Living (ADL’s) of Elderly Patients, falls and gait disorders. The framework
consists of four main components such as 3D LiDAR blender simulation, edge computing layer,
cloud computing layer and a patient activity monitoring web application. Algorithms for the
generation of simulated LiDAR data and data processing have been presented. The Raspberry
Pi 4 has been employed as the edge device along with Amazon Web Services for the cloud
computing layer. The IoT-LiDAR system has been tested for real-time performance. The results
data processing speed of the edge device is found to be 125ms and the end-to-end system
latency is 1.6 seconds. These results highlight the capability of the system to enable healthcare
professionals to rapidly respond to emergency situations and provide quality care to elderly
patients. This research thesis contributes to the field of healthcare by offering a non-obtrusive
privacy preserving solution to elderly patient activity monitoring in indoor environments. 

## Proposed Solution and High-Level System Architecture

![High-Level System Architecture of IoT-LiDAR system](Images/System%20Architecture.png)

## Novel 3D LiDAR Simulation using Blender

For the implementation of our IoT-LiDAR detection system, we required access to detailed
point cloud data ideally through data acquisition from a physical 3D LiDAR sensor installed
in an indoor environment and monitoring elderly participants. However, since we are aiming to
implement a proof of concept (PoC) demonstration of the IoT-LiDAR system, the above ideal
experimental setup would be too complex and unachievable with our given time constraints.
There was also the challenge of acquiring a 3D LiDAR sensor for research purposes, which
exceeded the projects budget and had very long shipping times. Also, at the time of conducting
this research, to our knowledge, there are no publicly available 3D LiDAR point cloud
datasets, that have specifically captured data of individuals performing Activities of Daily
Living (ADL’s), either in outdoor and indoor environments. Therefore, there was a significant
challenge of being able to collect 3D LiDAR point cloud data of humans performing activities,
without a physical LiDAR sensor and elderly participants. To solve this problem, we developed
a novel 3D LiDAR Simulation using Blender. The advantages of using a LiDAR simulation
to develop a proof-of-concept IoT-LiDAR system are numerous. The key advantages are
highlighted below:
1. Extremely Cost-Effective Solution: For developing the 3D LiDAR simulation, we use
Blender which is a free open-source 3D computer graphics and animation tool. The only
requirement to use this software is to have a Windows or Mac machine, which means
no expensive LiDAR hardware and real-world physical space is required and therefore
significantly reducing the effective cost of the project.
2. Significant Time Saving: To set up a physical indoor environment with furniture and
installation of 3D LiDAR hardware requires substantial amounts of time and planning.
In comparison, using a LiDAR simulation saves significant amount of time and can
easily be used for rapid prototyping and testing of the IoT-LiDAR system. The LiDAR
simulation can be used at any time during the day, whereas using a real-world indoor
environment would require permissions to access only at specific times and meet
scheduling requirements.
3. Eliminated Safety Concerns and is Ethical: In real-world experimental set up, we
would require having participants perform daily activities and carefully replicating falls
in the indoor environment. This raises ethical and safety concerns, which would require
collaboration with healthcare and legal professionals, to always ensure a safe environment
for the participants. By using a 3D LiDAR simulation, we have reduced the safety and
ethical concerns to zero, since no human participants is required nor harmed from the
simulation. The experiment is entirely run virtually on the computer.
4. Privacy Preserving Solution: The 3D LiDAR simulation is 100% privacy preserving,
where no personal or sensitive information about any individual is collected and stored.
5. Highly Scalable: The 3D LiDAR simulation is highly scalable, which means we can
create many simulations with indoor environments of varying dimensions and include
variety of furniture layouts to simulate real-world room variations. We can also animate
human models in Blender to perform various activities, and run the simulation as many
times as required to get high quality data to train deep learning models.



from neuromllite import Network, Cell, InputSource, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id='Example12_multicompartmental')
net.notes = 'Example 12: testing with multicompartmental cells...'

net.seed = 7890
net.temperature = 32

net.parameters = { 'N_pyr': 5, 'input_amp1':       0.3, 'input_amp2':       -0.2}

pyr_cell = Cell(id='pyr_4_sym', neuroml2_source_file='test_files/acnet2/pyr_4_sym.cell.nml')
net.cells.append(pyr_cell)


input_source = InputSource(id='poissonFiringSyn', neuroml2_source_file='test_files/inputs.nml')
net.input_sources.append(input_source)

input_source1 = InputSource(id='i_clamp1', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':'input_amp1', 'start':100, 'stop':300})

net.input_sources.append(input_source1)

input_source2 = InputSource(id='i_clamp2', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':'input_amp2', 'start':500, 'stop':800})

net.input_sources.append(input_source2)
                           

r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)

pop_pyr = Population(id='popPyr', size='N_pyr', component=pyr_cell.id, properties={'color':'.7 0 0'},random_layout = RandomLayout(region=r1.id))

net.populations.append(pop_pyr)

'''
net.synapses.append(Synapse(id='ampa', neuroml2_source_file='test_files/ampa.synapse.nml'))
net.synapses.append(Synapse(id='gaba', neuroml2_source_file='test_files/gaba.synapse.nml'))
                            
                            
net.projections.append(Projection(id='projEI',
                                  presynaptic=pE.id, 
                                  postsynaptic=pRS.id,
                                  synapse='ampa',
                                  delay=2,
                                  weight=0.2,
                                  random_connectivity=RandomConnectivity(probability=.8))'''
                                                    
                            
net.inputs.append(Input(id='stim',
                        input_source=input_source.id,
                        population=pop_pyr.id,
                        percentage=100,
                        segment_ids='[3,8]'))

print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='SimExample12',
                 network=new_file,
                 duration='1000',
                 seed='1111',
                 dt='0.025',
                 recordTraces={'all':'*:[0,1,2,3,4,5,6,7,8]'})
                 
sim.to_json_file()
print(sim.to_json())



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)

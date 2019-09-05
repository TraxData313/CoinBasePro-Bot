import numpy as np
import random
import time
import utils


'''
GLOBAL RULES:
- IMPORTANT! Inputs must be normalized! 0<x<1
- -0.5 < reward < 0.5

LOCAL RULES:
Encoding:
For every pair of connected cells a and b, on every tick check:
COV(a,b)  = C  , update EC
if b:
- R(a|b)  = Rp , update ERp
if !b:
- R(A|!b) = Rn , update ERn
for every matrix of connections, there are 3 more matrices: EC, ERp, ERn

Decoding:
Set every weight to:
R = ERp - ERn
w = R - EC*abs(R)

TESTS:
--- CHURN TEST RESULTS ---
- Churn test with parameters:
-- Hidden count  = 1
-- Hidden size   = 5
-- D_resist      = 1000
-- max_EF_resist = 500
-- for 2 epochs on smart reward:
--- +/- 0.50 for false positives
--- +/- 0.20 for false negatives
-- Result - 80% corrent with:
[[1425  170]  <- 10% false negatives
 [ 226  179]] <- 56% false positives

 
- Churn test with a deeper network:
-- Hidden count  = 2
-- Hidden size   = 20
-- D_resist      = 2000
-- max_EF_resist = 2000
-- for 5 epochs on smart reward
--- +/- 0.50 for false positives
--- +/- 0.16 for false negatives
-- Result - 70% corrent with:
[[1125  470]  <- 29% false negatives
 [ 143  262]] <- 35% false positives
 
 
- Churn test with even deeper network:
-- Hidden count  = 3
-- Hidden size   = 30
-- D_resist      = 2000
-- max_EF_resist = 2000
-- for 7 epochs on smart reward
--- +/- 0.50 for false positives
--- +/- 0.15 for false negatives
-- Result - 68% corrent with:
[[1091  504]  <- 31% false negatives
 [ 125  280]] <- 31% false positives

=> Scaling the network now increases the accuracy and avoids the confusion point!
--- END CHURN TEST RESULTS ---
'''







##################
# Class Network:
class Network:
    
    #######
    # INIT:
    def __init__(self,
                 input_size,
                 hidden_size,
                 output_size,
                 hidden_count,
                 is_RNN=0):
        # - Dimentions:
        self.hidden_count = hidden_count
        self.input_size   = input_size
        self.hidden_size  = hidden_size
        self.output_size  = output_size
        
        # - Parameters:
        self.is_RNN = is_RNN    # 0=ANN, 1=RNN
        self.RNN_reduce = 0.5  # on every turn reduce/weaken the PFs (0.5 reduces by 1/2)
        self.min_PF = 0.005
        self.max_PF = 0.995
        self.init_EF_resist   = 0
        self.max_EF_resist    = 1000
        self.D_resist         = 1000 # stationary connection resistance
        self.is_simple_connected = 0 # if 1 -> no LBC matrices exist
        self.is_chem_marking  = 0
        self.chem_decay       = 0.1
        
        # - Variables:
        self.life = 0
        self.EF_resist = self.init_EF_resist 
        
        # - Declare the cell layers:
        self.F_list    = [] # F  : Fired/notFired : 1/0
        self.PF_list   = [] # PF : Prob(Fire)
        self.EF_list   = [] # EF : MovingAverage(Fire)
        self.R_list    = [] # R  : Fire*Reward
        self.ER_list   = [] # ER : MovingAverage(Fire*Reward)
        self.Chem_list = [] # Marks fired cells
        
        # - Populate the cell layers:
        # -- Populate the input layers:
        temp_array = np.zeros(input_size)
        self.F_list.append(temp_array)
        temp_array = np.zeros(input_size)
        self.PF_list.append(temp_array)
        temp_array = np.zeros(input_size)
        self.EF_list.append(temp_array)
        temp_array = np.zeros(input_size)
        self.R_list.append(temp_array)
        temp_array = np.zeros(input_size)
        self.ER_list.append(temp_array)
        temp_array = np.zeros(input_size)
        self.Chem_list.append(temp_array)
        # -- Populate the hidden layers:
        for n in range(hidden_count):
            temp_array = np.zeros(hidden_size)
            self.F_list.append(temp_array)
            temp_array = np.zeros(hidden_size)
            self.PF_list.append(temp_array)
            temp_array = np.zeros(hidden_size)
            self.EF_list.append(temp_array)
            temp_array = np.zeros(hidden_size)
            self.R_list.append(temp_array)
            temp_array = np.zeros(hidden_size)
            self.ER_list.append(temp_array)
            temp_array = np.zeros(hidden_size)
            self.Chem_list.append(temp_array)
        
        # - Create the output layer:
        self.output_PF = np.zeros(output_size)
        self.output_F  = [] 
        
        # - Declare the connection matrices lists and the connection memory:
        self.LLC_list = [] # Layer-to-Layer      Connection matrices | List(Matrices)
        self.LLC_list_EC = []  # E(COV(a,b))
        self.LLC_list_ERp = [] # E(R(a|b))
        self.LLC_list_ERn = [] # E(R(a|!b))
        
        if self.is_simple_connected == 0:
            self.LBC_list = [] # Layer-to-Backlayers Connection matrices | List(Lists(Matrices))
            self.LBC_list_EC = []
            self.LBC_list_ERp = []
            self.LBC_list_ERn = []
        
        self.LOC_list = [] # Layer-to-Output     Connection matrices | List(Matrices)
        self.LOC_list_EC = []
        self.LOC_list_ERp = []
        self.LOC_list_ERn = []
        
        # - Populate the LLC_list:
        for n in range (hidden_count):
            rows = len(self.F_list[n])
            cols = len(self.F_list[n+1])
            # - Connections:
            temp_matrix = utils.diagonalized(rows, cols, min=-0.2, max=0.2)
            self.LLC_list.append(temp_matrix)
            # - Memory:
            temp_matrix = np.zeros((rows, cols))
            self.LLC_list_EC.append(temp_matrix)
            temp_matrix = np.zeros((rows, cols))
            self.LLC_list_ERp.append(temp_matrix)
            temp_matrix = np.zeros((rows, cols))
            self.LLC_list_ERn.append(temp_matrix)
            
        # - Populate the LBC_list:
        if self.is_simple_connected == 0:
            for n in range (hidden_count):
                # -- For every cell layer, create a matrix list of lenght n:
                temp_matrix_list = []
                temp_LBC_list_EC = []
                temp_LBC_list_ERp = []
                temp_LBC_list_ERn = []
                for k in range(n):
                    # A[n] dot A[k] for k from 0 up to n-1:
                    rows = len(self.F_list[n]) 
                    cols = len(self.F_list[n-1-k])
                    # - Connections:
                    temp_matrix = utils.diagonalized(rows, cols, min=-0, max=0)
                    temp_matrix_list.append(temp_matrix)
                    # - Memory:
                    temp_matrix = np.zeros((rows, cols))
                    temp_LBC_list_EC.append(temp_matrix)
                    temp_matrix = np.zeros((rows, cols))
                    temp_LBC_list_ERp.append(temp_matrix)
                    temp_matrix = np.zeros((rows, cols))
                    temp_LBC_list_ERn.append(temp_matrix)
                self.LBC_list.append(temp_matrix_list)
                self.LBC_list_EC.append(temp_LBC_list_EC)
                self.LBC_list_ERp.append(temp_LBC_list_ERp)
                self.LBC_list_ERn.append(temp_LBC_list_ERn)
        
        # - Populate the LOC_list:
        for n in range (hidden_count+1):
            rows = len(self.F_list[n])
            cols = len(self.output_PF)
            temp_matrix = utils.diagonalized(rows, cols, min=-0.2, max=0.2)
            self.LOC_list.append(temp_matrix)
            temp_matrix = np.zeros((rows, cols))
            self.LOC_list_EC.append(temp_matrix)
            temp_matrix = np.zeros((rows, cols))
            self.LOC_list_ERp.append(temp_matrix)
            temp_matrix = np.zeros((rows, cols))
            self.LOC_list_ERn.append(temp_matrix)
    # END INIT
    ##########
    
    
    ############
    # Operators:

    ### ### ###
    ### Get Input and Propagate:
    
    # ROADMAP for Input and Propagate:
    # - Decay the chem markings
    # - Reset Fs
    # - Reset PFs and output layer if is_RNN=0
    # - Reduce the PFs and output layer if is_RNN=1
    # - Iterate all layers:
        # -- For layer == 0: 
            # --- get input into PF
            # --- F = bound(PF)
        # -- For layer  > 0: 
            # --- decide whether to F | PF
        # -- Run LL connections PF[n+1]   += F[n] * LL[n]
        # -- Run LB connections PF[n-1-k] += F[n] * LB[n][k]
            # --- Run LB[k]
            # --- Force re-fire on F[n-1-k]
                # ---- For input layer F = bound(PF)
                # ---- For hidden layers decide whether to F | PF
    # - Run LO connections PF[out] += F[n] * LO[n]
    # - Check the fired cells and update the chem markings
    # - Update all EFs
    # - Increase the EF_resist
    # - Provide the output
    # - Update life
    
    # IMPLEMENTATION of Input and Propagate:
    def getInputAndPropagate(self,input_array):
        # - Decay the chem markings:
        if self.is_chem_marking == 1:
            for layer in range(self.hidden_count+1):
                for cell in range(len(self.Chem_list[layer])):
                    self.Chem_list[layer][cell] = self.Chem_list[layer][cell] - self.chem_decay
                    if self.Chem_list[layer][cell] < 0.0:
                        self.Chem_list[layer][cell] = 0.0
    
        # - Reset Fs:
        for layer in range(self.hidden_count+1):
            self.F_list[layer] = np.zeros(len(self.F_list[layer]))
            
        # - Reset PFs and output layer if is_RNN=0:
        if self.is_RNN == 0:
            for layer in range(self.hidden_count+1):
                self.PF_list[layer] = np.zeros(len(self.PF_list[layer]))
            self.output_PF = np.zeros(self.output_size)
            
        # - Reduce the PFs and output layer if is_RNN=1:
        if self.is_RNN == 1:
            for layer in range(self.hidden_count+1):
                self.PF_list[layer] = np.multiply(self.PF_list[layer],self.RNN_reduce)
            self.output_PF = self.output_PF*self.RNN_reduce
            
        # - Iterate all layers:
        for layer in range(self.hidden_count+1):
            # -- For layer == 0:
            if layer == 0:
                # --- get input into PF:
                self.PF_list[layer] = input_array
                # --- F = bound(PF)
                #self.F_list[layer]  = utils.boundInputMinMaxArray(self.PF_list[layer], 0, 1)
                
                # --- F = PF:
                self.F_list[layer] = self.PF_list[layer]
                
            # -- For layer  > 0: 
            if layer  > 0:
                # --- decide whether to F | PF:
                self.F_list[layer] = utils.fireNotFire(self.PF_list[layer], self.min_PF, self.max_PF)
            # -- Run LL connections PF[n+1]   += F[n] * LL[n]
            for n in range(self.hidden_count):
                self.PF_list[n+1] += np.dot(self.F_list[n], self.LLC_list[n])
                
            # -- Run LB connections PF[n-1-k] += F[n] * LB[n][k]
            if self.is_simple_connected == 0:
                for n in range(self.hidden_count):
                    # --- Run LB[k]
                    for k in range(n):
                        self.PF_list[n-1-k] += np.dot(self.F_list[n], self.LBC_list[n][k])
                        # ---- Force re-fire on F[n-1-k]
                        # ----- For input layer Set F = bound(PF):
                        if n-1-k == 0:
                            self.F_list[0] = utils.boundInputMinMaxArray(self.PF_list[0], 0, 1)
                        # ----- For hidden layers decide whether to F | PF:
                        else:
                            self.F_list[n-1-k] = utils.fireNotFire(self.PF_list[n-1-k], self.min_PF, self.max_PF)
                            
        # - Run LO connections PF[out] += F[n] * LO[n]
        for n in range(self.hidden_count+1):
            self.output_PF += np.dot(self.F_list[n], self.LOC_list[n])
        
        # - Check the fired cells and update the chem markings:
        if self.is_chem_marking == 1:
            for layer in range(self.hidden_count+1):
                for cell in range(len(self.Chem_list[layer])):
                    if self.F_list[layer][cell] == 1:
                        self.Chem_list[layer][cell] = 1
        
        # - Update all EFs:
        for layer in range(self.hidden_count+1):
            for el in range(len(self.F_list[layer])):
                old_value = self.EF_list[layer][el]
                new_value = self.F_list[layer][el]
                resistance = self.EF_resist
                self.EF_list[layer][el] = utils.movingAverage(old_value, new_value, resistance)
        
        # - Increase the EF_resist:
        self.EF_resist += 1
        if self.EF_resist > self.max_EF_resist:
            self.EF_resist = self.max_EF_resist
            
        # - Provide the output:
        self.output_F = utils.classOutput(self.output_PF, self.min_PF, self.max_PF)
        
        # - Update life:
        self.life = self.life + 1
    ### END Get Input and Propagate
    ### ### ###
   
    ### ### ###
    ### Get Reward and Update:
    
    # ROADMAP for Reward and Update:
    # - Calculate the Rs (skipping ERs for now)
    # - For all connection matrices:
        # -- Calculate the ERp or ERn
        # -- Calculate the EC
        # -- Update and bound (-1 < w < 1) the weight
        
    # IMPLEMENTATION of Reward and Update:
    def rewardAndUpdate(self, reward):
        
        # - Calculate the Rs:
        for layer in range(self.hidden_count+1):
            if self.is_chem_marking == 1:
                self.R_list[layer] = np.multiply(self.Chem_list[layer], reward)
            else:
                self.R_list[layer] = np.multiply(self.F_list[layer], reward)
                
        # - For all connection matrices:
        # -- LLC_list, PF[n+1] += F[n] * LL[n]:
        for n in range(self.hidden_count):
            # -- Calculate the ERp or ERn:
            source_array = self.F_list[n]
            target_array = self.F_list[n+1]
            ERp_matrix   = self.LLC_list_ERp[n]
            ERn_matrix   = self.LLC_list_ERn[n]
            resist       = self.D_resist
            self.LLC_list_ERp[n], self.LLC_list_ERn[n] = utils.updERpAndERn(source_array, target_array, ERp_matrix, ERn_matrix, reward, resist)
            # -- Calculate the EC:
            A_array   = self.F_list[n]
            EA_array  = self.EF_list[n]
            B_array   = self.F_list[n+1]
            EB_array  = self.EF_list[n+1]
            EC_matrix = self.LLC_list_EC[n]
            self.LLC_list_EC[n] = utils.updEC(A_array, EA_array, B_array, EB_array, EC_matrix, resist)
            # -- Update and bound (-1 < w < 1) the weight:
            W_matrix   = self.LLC_list[n]
            ERp_matrix = self.LLC_list_ERp[n]
            ERn_matrix = self.LLC_list_ERn[n]
            EC_matrix  = self.LLC_list_EC[n]
            self.LLC_list[n] = utils.updWeightBound(W_matrix, ERp_matrix, ERn_matrix, EC_matrix)
            
        if self.is_simple_connected == 0:
            # -- LBC_list, PF[n-1-k] += F[n] * LB[n][k]:
            for n in range(self.hidden_count):
                for k in range(n):
                    # -- Calculate the ERp or ERn:
                    source_array = self.F_list[n]
                    target_array = self.F_list[n-1-k]
                    ERp_matrix   = self.LBC_list_ERp[n][k]
                    ERn_matrix   = self.LBC_list_ERn[n][k]
                    resist       = self.D_resist
                    self.LBC_list_ERp[n][k], self.LBC_list_ERn[n][k] = utils.updERpAndERn(source_array, target_array, ERp_matrix, ERn_matrix, reward, resist)
                    # -- Calculate the EC:
                    A_array   = self.F_list[n]
                    EA_array  = self.EF_list[n]
                    B_array   = self.F_list[n-1-k]
                    EB_array  = self.EF_list[n-1-k]
                    EC_matrix = self.LBC_list_EC[n][k]
                    self.LBC_list_EC[n][k] = utils.updEC(A_array, EA_array, B_array, EB_array, EC_matrix, resist)
                    # -- Update and bound (-1 < w < 1) the weight:
                    W_matrix   = self.LBC_list[n][k]
                    ERp_matrix = self.LBC_list_ERp[n][k]
                    ERn_matrix = self.LBC_list_ERn[n][k]
                    EC_matrix  = self.LBC_list_EC[n][k]
                    self.LBC_list[n][k] = utils.updWeightBound(W_matrix, ERp_matrix, ERn_matrix, EC_matrix)
            
        # -- LOC_list, PF[out] += F[n] * LO[n]
        for n in range(self.hidden_count+1):
            # -- Calculate the ERp or ERn:
            source_array = self.F_list[n]
            target_array = self.output_F
            ERp_matrix   = self.LOC_list_ERp[n]
            ERn_matrix   = self.LOC_list_ERn[n]
            resist       = self.D_resist
            self.LOC_list_ERp[n], self.LOC_list_ERn[n] = utils.updERpAndERn(source_array, target_array, ERp_matrix, ERn_matrix, reward, resist)
            # -- Calculate the EC:
            A_array   = self.F_list[n]
            EA_array  = self.EF_list[n]
            B_array   = self.output_F
            EB_array  = self.output_PF
            EC_matrix = self.LOC_list_EC[n]
            self.LOC_list_EC[n] = utils.updEC(A_array, EA_array, B_array, EB_array, EC_matrix, resist)
            # -- Update and bound (-1 < w < 1) the weight:
            W_matrix   = self.LOC_list[n]
            ERp_matrix = self.LOC_list_ERp[n]
            ERn_matrix = self.LOC_list_ERn[n]
            EC_matrix  = self.LOC_list_EC[n]
            self.LOC_list[n] = utils.updWeightBound(W_matrix, ERp_matrix, ERn_matrix, EC_matrix)
    
    ### END Get Reward and Update
    ### ### ###
    
    ### ### ###
    ### returnOutputPlace:
    def returnOutputPlace(self):
        for n in range(self.output_size):
            if self.output_F[n] == 1:
                output_place = n        
        return output_place
    
    ### END returnOutputPlace
    ### ### ###
    
    # END Operators
    ###############

    
    #################
    # Representators:
    # - __repr__:
    def __repr__(self):
        return "R: {} -> {}x{} -> {}".format(self.input_size, 
                                             self.hidden_count, 
                                             self.hidden_size,
                                             self.output_size)
    # - Print cell layers:
    def printFlist(self):
        print()
        print("- Current Fired cells:")
        for n in range(self.hidden_count+1):
            print(self.F_list[n])
    def printPFlist(self):
        print()
        print("- Current Probability of Fire:")
        for n in range(self.hidden_count+1):
            print(self.PF_list[n])
    def printEFlist(self):
        print()
        print("- Average Fire State:")
        for n in range(self.hidden_count+1):
            print(self.EF_list[n])
    def printRlist(self):
        print()
        print("- Rewarded Cells:")
        for n in range(self.hidden_count+1):
            print(self.R_list[n])
    def printERlist(self):
        print()
        print("- Average Reward:")
        for n in range(self.hidden_count+1):
            print(self.ER_list[n])
    def printOutputLayer(self):
        print()
        print("- Output Layer PF and F:")
        print(self.output_PF)
        print(self.output_F)
    # - Print connection matrices:
    def printLLClist(self):
        print()
        print("- LLC matrices:")
        for n in range(self.hidden_count):
            print(self.LLC_list[n])
            print()
    def printLBClist(self):
        print()
        print("- LBC matrices:")
        for n in range(self.hidden_count):
            print("-- LBC matrices for layer", n, ":")
            if n == 0:
                print("None")
                print()
            for k in range(n):
                print(self.LBC_list[n][k])
                print()
    def printLOClist(self):
        print()
        print("- LOC matrices:")
        for n in range(self.hidden_count+1):
            print(self.LOC_list[n])
            print()
    # END Representators
    ####################


# END Class Network
#####################











































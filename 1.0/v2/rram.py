import numpy as np

class rram:
    def __init__(self, shape, gap_min, gap_max, gap_ini, T_ini, deltaGap0, model_switch):
        self.shape = shape
        
        # Switch to select Standard Model (0) or Dynamic Model (1)
        # parameter integer	model_switch		= 0    from[0, 1];
        self.model_switch = model_switch
  
        # Boltzmann's constant in joules/kelvin, 'kb =  1.3806503e-23'
        self.kb = 1.3806503e-23

        # charge of electron in coulombs, 'q =  1.6e-19'
        self.q = 1.6e-19

        # average switching fitting parameters g0, V0, I0, beta, gamma0
        # parameter real		g0		= 0.25e-9 from(0:2e-9);
        self.g0 = 0.375e-9
        # parameter real		V0		= 0.25    from(0:10);
        self.V0 = 0.25
        # parameter real		Vel0		= 10    from(0:20);
        self.Vel0 = 10
        # parameter real		I0		= 1000e-6 from(0:1e-2);
        self.I0 = 1e-6
        # parameter real		beta		= 0.8    from(0:inf);
        self.beta = 0.8
        # parameter real		gamma0		= 16  from(0:inf); 
        self.gamma0 = np.ones(shape=self.shape) * 16.

        # threshold temperature for significant random variations
        # parameter real		T_crit		= 450		from(390, 460);
        self.T_crit = 450

        # variations fitting parameters
        # parameter real          deltaGap0	= 0.1		from[0, inf);
        self.deltaGap0 = deltaGap0
        # parameter real		T_smth		= 500		from(400, 600);
        self.T_smth = 500
        # acitivated energy of Vo in HfOx
        # parameter real		Ea		= 0.6 from(0:1);
        self.Ea = 0.6

        # atom spacing, a0
        # parameter real		a0		= 0.25e-9 from(0:inf);
        self.a0 = 0.25e-9
        self.a = 0
        # initial room temperature in devices
        # parameter real		T_ini		= 273 + 25 from(0:inf);
        self.T_ini = T_ini
        # minimum field requirement to enhance gap formation, F_min
        # parameter real		F_min		= 1.4e9 from(0:3e9);
        self.F_min = 1.4e9
        # initial gap distance, gap_ini
        # parameter real		gap_ini		= 2e-10 from(0:100e-10);
        self.gap_ini = gap_ini
        # minimum gap distance, gap_min
        # parameter real		gap_min		= 2e-10 from(0:100e-10);
        self.gap_min = gap_min
        # maximum gap distance, gap_max
        # parameter real		gap_max		= 14e-10 from(0:100e-10);
        self.gap_max = gap_max
        # thermal resistance
        # parameter real		Rth		= 2.1e3 from(0:inf);
        self.Rth = 2.1e3
        # oxide thickness, thickness
        # parameter real		tox		= 12e-9 from(0:100e-9);
        self.tox = 12e-9

        # voltage V(TE, BE), Vtb; current I(TE, BE), Itb
        self.Vtb = 0.
        self.Itb = 0.

        # present temperature in devices, temp
        self.T_cur = 0.

        # gap time derivative, gap_ddt; random gap time derivative, gap_random_ddt
        self.gap_ddt = 0.
        self.gap_random_ddt = 0.

        # present gap status
        self.gap = np.ones(shape=self.shape) * self.gap_ini

        # local enhancement factor, gamma
        self.gamma = np.zeros(shape=self.shape)
        self.gamma_ini = np.zeros(shape=self.shape)

        #  random number
        self.random_seed = 0
        self.deltaGap = 0.

    def step(self, Vin, dt):
        assert(np.shape(Vin) == self.shape)

        self.Vtb = Vin

        # Itb = I(TE,BE);
        # dont reset this to zero !!
        # self.Itb = 0 
        # it has very little effect anyways.

        # T_cur = T_ini + abs( Vtb * Itb * Rth);
        self.T_cur = self.T_ini + abs( self.Vtb * self.Itb * self.Rth)
        
        self.gamma_ini = self.gamma0
        
        idx = np.where(self.Vtb < 0.)
        self.gamma_ini[idx] = 16.
		        
        self.gamma = self.gamma_ini-self.beta*np.power(((self.gap)/1e-9), 3)
		
        idx = np.where((self.gamma*np.abs(self.Vtb)/self.tox) < self.F_min)
        self.gamma[idx] = 0.
		
        # calculate next time step gap situation
        # gap time derivative - determinant part
        self.a = self.a0/np.power((self.T_cur/298), 0.95)
        #self.gap_ddt = -self.Vel0*np.exp(-self.q*self.Ea/self.kb/self.T_cur)*np.sinh(self.gamma*self.a/self.tox*self.q*self.Vtb/self.kb/self.T_cur)
        self.gap_ddt = -self.Vel0*(np.exp(-self.q*(self.Ea+1e-12)/self.kb/self.T_cur)*np.exp(self.gamma*self.a/self.tox*self.q*self.Vtb/self.kb/self.T_cur) - np.exp(-self.q*self.Ea/self.kb/self.T_cur)*np.exp(-self.gamma*self.a/self.tox*self.q*self.Vtb/self.kb/self.T_cur))/2

        # gap time derivative - variation part
		# deltaGap = deltaGap0 * model_switch;
        self.deltaGap = self.deltaGap0 * self.model_switch
		
		# gap_random_ddt = $rdist_normal(rand_seed, 0, 1) * deltaGap / (1 + exp((T_crit - T_cur)/T_smth));
        self.gap_random_ddt = np.random.uniform(-1., 1.)*self.deltaGap/(1.+np.exp((self.T_crit-self.T_cur)/self.T_smth))
        #self.gap_random_ddt = 0.
		
        self.gap += (self.gap_ddt + self.gap_random_ddt)*dt
        self.gap = np.clip(self.gap, self.gap_min, self.gap_max)
		    
        self.Itb = self.I0 * np.exp(-self.gap/self.g0)*self.Vtb #np.sinh(self.Vtb / self.V0)

        assert(np.shape(self.Itb) == self.shape)

        return self.Itb, self.T_cur
    
    def R(self, Vread=None):
        if Vread == None:
            R_out = 1./(self.I0*np.exp(-self.gap/self.g0)+1e-12)
        else:
            R_out = Vread/(self.I0*np.exp(-self.gap/self.g0)+1e-12)
            
        return R_out

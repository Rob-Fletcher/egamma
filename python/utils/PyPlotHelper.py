

class PyPlotHelper:
   def __init__(self):
      self.varBoundariesLow  = {'el_deltaeta1':  -0.02
                                ,'el_f0':        -0.1
                                ,'el_f1':        -0.1 
                                ,'el_f3':        -0.02
                                ,'el_fside':     -0.2
                                ,'el_deltaphi2': -0.1
                                ,'el_reta':       0.5
                                ,'el_rhad':      -0.075
                                ,'el_rphi':       0.45
                                ,'el_weta2':      0.006
                                ,'el_wstot':      0.
                                ,'el_ws3':        0.3
                                ,'el_d0Sig':      0.
                                ,'el_d0significance':      0.
                                ,'el_TRTHighTHitsRatio':0.0
                                ,'el_TRTHighTOutliersRatio':0.0
                                ,'el_trackd0':   -1.
                                ,'el_trackd0pvunbiased':   -0.3
                                ,'el_deltaEmax2': 0. # good
                                ,'el_eratio': 0. # good
                                ,'el_ptcone20pt': 0.
                                ,'el_EoverP':     0.
                                ,'el_PassBL':     0.
                                ,'el_deltaphiRescaled':-0.03
                                ,'el_DeltaPoverP':-0.2
                                ,'el_MVAResponse':-1.5
                                ,'el_cl_phi'     :-3.1416
                                }
      
      self.varBoundariesHi  = {'el_deltaeta1':   0.02
                               ,'el_f0':         0.5
                               ,'el_f1':         0.65
                               ,'el_f3':         0.15
                               ,'el_fside':      1.5
                               ,'el_deltaphi2':  0.05
                               ,'el_reta':       1.5
                               ,'el_rhad':       0.2
                               ,'el_rphi':       1.05
                               ,'el_weta2':      0.018
                               ,'el_wstot':      8.
                               ,'el_ws3':        1.
                               ,'el_d0Sig':     20.
                               ,'el_d0significance':     20.
                               ,'el_TRTHighTHitsRatio':0.5
                               ,'el_TRTHighTOutliersRatio':0.5
                               ,'el_trackd0':    1.
                               ,'el_trackd0pvunbiased':    0.3
                               ,'el_deltaEmax2': 1. # good
                               ,'el_eratio': 1. # good
                               ,'el_ptcone20pt': 0.5
                               ,'el_EoverP':     8.
                               ,'el_PassBL':     2.
                               ,'el_deltaphiRescaled':0.03
                               ,'el_DeltaPoverP':1.2
                               ,'el_MVAResponse':1.
                               ,'el_cl_phi'     :3.1416
                               }

      self.varBins          = {'el_deltaeta1':   300
                               ,'el_f0':         300
                               ,'el_f1':         150
                               ,'el_f3':         200
                               ,'el_fside':      300
                               ,'el_deltaphi2':  300
                               ,'el_reta':       300
                               ,'el_rhad':       300
                               ,'el_rphi':       200
                               ,'el_weta2':      150
                               ,'el_wstot':      300
                               ,'el_ws3':        300
                               ,'el_d0Sig':     300
                               ,'el_d0significance':     300
                               ,'el_TRTHighTHitsRatio':300
                               ,'el_TRTHighTOutliersRatio':50
                               ,'el_trackd0':    300
                               ,'el_trackd0pvunbiased':    300
                               ,'el_deltaEmax2': 300 # good
                               ,'el_eratio': 300 # good
                               ,'el_ptcone20pt': 300
                               ,'el_EoverP':     300
                               ,'el_PassBL':     300
                               ,'el_deltaphiRescaled':300
                               ,'el_DeltaPoverP':300
                               ,'el_MVAResponse':300
                               ,'el_cl_phi'     :300
                               }

      self.detLow            = {'lar_em':
                                    { 'PS':
                                        { 'eta' : -2.5,
                                          'phi' : -3.142
                                        },
                                     'layer_1':
                                        { 'eta' : -2.5,
                                          'phi' : -3.142
                                        },
                                     'layer_2' :
                                        { 'eta' : -2.5,
                                          'phi' : -3.142
                                        },
                                     'layer_3' :
                                        { 'eta' : -2.5,
                                          'phi' : -3.142
                                        },
                                     'ec_in_PS':      #### Need to set up the bounds for the endcap hisotrams
                                       { 'eta' : -2.5,  
                                         'phi' : -3.142
                                       },
                                     'ec_in_l1':
                                       { 'eta' : -2.5,
                                         'phi' : -3.142
                                       },
                                     'ec_in_l2' :
                                       { 'eta' : -2.5,
                                         'phi' : -3.142
                                       },
                                     'ec_in_l3' :
                                       { 'eta' : -2.5,
                                         'phi' : -3.142
                                       },
                                     'ec_out_PS':
                                       { 'eta' : -2.5,
                                         'phi' : -3.142
                                       },
                                     'ec_out_l1':
                                       { 'eta' : -2.5,
                                         'phi' : -3.142
                                       },
                                     'ec_out_l2' :
                                       { 'eta' : -2.5,
                                         'phi' : -3.142
                                       },
                                     'ec_out_l3' :
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },

                                    },
                                'tile' :
                                    { 'sample_a':
                                        { 'eta': -2.5,
                                          'phi': -3.142
                                        },
                                      'sample_b':
                                         { 'eta': -2.5,
                                           'phi': -3.142
                                         },                                       
                                      'sample_d':
                                         { 'eta': -2.5,
                                           'phi': -3.142
                                         },                                     
                                      'sample_e':
                                         { 'eta': -2.5,
                                           'phi': -3.142
                                         },
                                      'sample_x':
                                        { 'eta': -2.5,
                                          'phi': -3.142
                                        }

                                    }
                                }

      self.detHi             = {'lar_em':
                                    { 'PS':
                                        { 'eta' : 2.5,
                                          'phi' : 3.142
                                        },
                                     'layer_1':
                                        { 'eta' : 2.5,
                                          'phi' : 3.142
                                        },
                                     'layer_2' :
                                        { 'eta' : 2.5,
                                          'phi' : 3.142
                                        },
                                     'layer_3' :
                                        { 'eta' : 2.5,
                                          'phi' : 3.142
                                        },
                                     'ec_in_PS':
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_in_l1':
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_in_l2' :
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_in_l3' :
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_out_PS':
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_out_l1':
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_out_l2' :
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                     'ec_out_l3' :
                                       { 'eta' : 2.5,
                                         'phi' : 3.142
                                       },
                                    },
                                'tile' :
                                    { 'sample_a':
                                        { 'eta': 2.5,
                                          'phi': 3.142
                                        },
                                      'sample_b':
                                         { 'eta': 2.5,
                                           'phi': 3.142
                                         },                                       
                                      'sample_d':
                                         { 'eta': 2.5,
                                           'phi': 3.142
                                         },                                     
                                      'sample_e':
                                        { 'eta': 2.5,
                                          'phi': 3.142
                                        },
                                      'sample_x':
                                        { 'eta': 2.5,
                                          'phi': 3.142
                                        }

                                    }
                                }

      self.detBins           = {'lar_em':
                                    { 'PS':
                                        { 'eta' : 200,
                                          'phi' : 64
                                        },
                                     'layer_1':
                                        { 'eta' : 1600,
                                          'phi' : 64
                                        },
                                     'layer_2' :
                                        { 'eta' : 200,
                                          'phi' : 256
                                        },
                                     'layer_3' :
                                        { 'eta' : 100,
                                          'phi' : 256
                                        },
                                    },
                                'tile' :
                                    { 'sample_a':
                                        { 'eta': 50,
                                          'phi': 64
                                        },
                                      'sample_b':
                                         { 'eta': 50,
                                           'phi': 64
                                         },                                       
                                      'sample_d':
                                         { 'eta': 50,
                                           'phi': 64
                                         },                                     
                                      'sample_e':
                                        { 'eta': 50,
                                          'phi': 64
                                        },
                                      'sample_x':
                                        { 'eta': 50,
                                          'phi': 64
                                        }
                                    }
                                }


   def getBins(self, var):
      return self.varBins[var]

   def getLow(self,var):
      return self.varBoundariesLow[var]

   def getHi(self,var):
      return self.varBoundariesHi[var]

   def getDetLow(self, det, layer, coord):
      return self.detLow[det][layer][coord]

   def getDetHi(self, det, layer, coord):
      return self.detHi[det][layer][coord]

   def getDetBins(self, det, layer, coord):
      return self.detBins[det][layer][coord]


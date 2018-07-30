"""Python EpanetMSXToolkit interface
Junli Hao 07/29/2018"""
import ctypes
import platform
import datetime
import os

'''
LIST OF FUNCTIONS:
msx.MSXopen(msx_file)
msx.MSXaddpattern(pattern_name)
msx.MSXsetpattern(pattern_index,[multipliers])
msx.MSXsetpatternvalue(pattern_index,time_index,value)
msx.MSXsetconstant(constant_index,value)
msx.MSXsetparameter(location_type,location_index,parameter_index,value)
msx.MSXsetinitqual(location_type,location_index,species_index,value)
msx.MSXsetsource(node_index,species_index,source_type,value,pattern_index)
index = msx.MSXgetindex(object_type,object_label)
label = msx.MSXgetID(object_type,object_index)
length = msx.MSXgetIDlen(object_type,object_index)
initqual = msx.MSXgetinitqual(location_type,location_index,species_index)
qual = msx.MSXgetqual(location_type,location_ind,species_ind)
constant = msx.MSXgetconstant(constant_index)
parameter = msx.MSXgetparameter(location_type,location_index,parameter_index)
[type,value,pattern] = msx.MSXgetsource(node_index,species_index)
length = msx.MSXgetpatternlen(pattern_index)
value = msx.MSXgetpatternvalue(pattern_index,time_index)
[type,units,aTol,rTol] = msx.MSXgetspecies(species_index)
count = msx.MSXgetcount(object_index)
msx.MSXusehydfile(hydfile)
msx.MSXinit()
[t,t_left] = msx.MSXstep()
msx.MSXsolveH()
msx.MSXsolveQ()
msx.MSXreport()
msx.MSXsaveoutfile(binfile)
msx.MSXsavemsxfile(new_msx_inpfile)
msx.MSXclose()

 // MSX constants
# object type
MSX_NODE      0
MSX_LINK      1
MSX_TANK      2
MSX_SPECIES   3
MSX_TERM      4
MSX_PARAMETER 5
MSX_CONSTANT  6
MSX_PATTERN   7
# location type
MSX_BULK      0
MSX_WALL      1
# source type
MSX_NOSOURCE  -1
MSX_CONCEN     0
MSX_MASS       1
MSX_SETPOINT   2
MSX_FLOWPACED  3
'''

# os.chdir('C:\Users\User1\Dropbox (MIT)\\2018 Mekorot\Python EPANET wrapper\epanet-module')
# ctypes.windll.kernel1.SetDllDirectoryW(None)
_plat= platform.system()
if _plat=='Windows':
    os.environ['PATH'] = os.path.dirname(__file__) + ';' + os.environ['PATH']
    try:
        # if epanetmsx.dll compiled with __cdecl (as in OpenWaterAnalytics)
        _lib = ctypes.CDLL("epanetmsx.dll")
    except ValueError:
        # if epanetmsx.dll compiled with __stdcall (as in EPA original DLL)
        try:
            _lib = ctypes.windll.epanetmsx
        except ValueError:
            raise Exception("epanetmsx.dll not suitable")

else:
    Exception('Platform '+ _plat +' unsupported (not yet)')


#----------running the simulation-----------------------------------------------------
def MSXopen(nomeinp):
    """Opens the MSX Toolkit to analyze a particular distribution system
    Arguments:
    nomeinp: name of the msx input file
    """
    ierr= _lib.MSXopen(ctypes.c_char_p(nomeinp.encode()))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXclose():
  """Closes down the Toolkit system (including all files being processed)"""
  ierr= _lib.MSXclose()
  if ierr!=0: raise MSXtoolkitError(ierr)

def MSXusehydfile(fname):
    """Uses the contents of the specified file as the current binary hydraulics file"""
    ierr = _lib.MSXusehydfile(ctypes.c_char_p(fname.encode()))
    if ierr != 0: raise MSXtoolkitError(ierr)

def MSXsolveH():
    """Runs a complete hydraulic simulation with results
    for all time periods written to the binary Hydraulics file."""
    ierr = _lib.MSXsolveH()
    if ierr != 0: raise MSXtoolkitError(ierr)

def MSXinit(saveFlag=0):
    """Initializes the MSX system before solving for water quality results in step-wise fashion
    set saveFlag to 1 if water quality results should be saved to a scratch binary file, or to 0 is not saved to file"""
    ierr = _lib.MSXinit(saveFlag)
    if ierr != 0: raise MSXtoolkitError(ierr)

def MSXsolveQ():
    """solves for water quality over the entire simulation period and saves the results to an internal scratch file"""
    ierr = _lib.MSXsolveQ()
    if ierr != 0: raise MSXtoolkitError(ierr)

def MSXstep():
    """Advances the water quality simulation one water quality time step.
    The time remaining in the overall simulation is returned as tleft, the current time as t."""
    t = ctypes.c_long()
    tleft = ctypes.c_long()
    ierr = _lib.MSXstep(ctypes.byref(t),ctypes.byref(tleft))
    if ierr != 0: raise MSXtoolkitError(ierr)
    out = [t.value, tleft.value]
    return out

def MSXsaveoutfile(fname):
    """saves water quality results computed for each node, link and reporting time period to a named binary file"""
    ierr = _lib.MSXsaveoutfile(ctypes.c_char_p(fname.encode()))
    if ierr != 0: raise MSXtoolkitError(ierr)

def MSXsavemsxfile(fname):
    """saves the data associated with the current MSX project into a new MSX input file"""
    ierr = _lib.MSXsavemsxfile(ctypes.c_char_p(fname.encode()))
    if ierr != 0: raise MSXtoolkitError(ierr)

def MSXreport():
    """ Writes water quality simulations results as instructed by the MSX input file to a text file"""
    ierr = _lib.MSXreport()
    if ierr != 0: raise MSXtoolkitError(ierr)

#---------get parameters---------------------------------------------------------------
def MSXgetindex(type,name):
    """Retrieves the internal index of an MSX object given its name.
    Arguments:
    type (int)
    MSX_SPECIES - 3 (for a chemical species)
    MSX_CONSTANT - 6 (for a reaction constant
    MSX_PARAMETER - 5 (for a reaction parameter)
    MSX_PATTERN - 7 (for a time pattern)"""
    type_ind = 100  # in case the type input is in text
    if type == 'MSX_SPECIES' or type == 3:
        type_ind = 3
    if type == 'MSX_CONSTANT' or type == 6:
        type_ind = 6
    if type == 'MSX_PARAMETER' or type == 5:
        type_ind = 5
    if type == 'MSX_PATTERN' or type == 7:
        type_ind = 7
    if type_ind == 100: raise Exception('unrecognized type')
    ind = ctypes.c_int()
    ierr= _lib.MSXgetindex(type_ind,ctypes.c_char_p(name.encode()),ctypes.byref(ind))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return ind.value

def MSXgetIDlen(type,index):
    """Retrieves the number of characters in the ID name of an MSX object given its internal index number.
    Arguments:
    type - int:
    MSX_SPECIES - 3 (for a chemical species)
    MSX_CONSTANT - 6 (for a reaction constant
    MSX_PARAMETER - 5 (for a reaction parameter)
    MSX_PATTERN - 7 (for a time pattern)"""
    type_ind = 100  # in case the type input is in text
    if type == 'MSX_SPECIES' or type == 3:
        type_ind = 3
    if type == 'MSX_CONSTANT' or type == 6:
        type_ind = 6
    if type == 'MSX_PARAMETER' or type == 5:
        type_ind = 5
    if type == 'MSX_PATTERN' or type == 7:
        type_ind = 7
    if type_ind == 100: raise Exception('unrecognized type')
    len = ctypes.c_int()
    ierr= _lib.MSXgetIDlen(type_ind,ctypes.c_int(index),ctypes.byref(len))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return len.value

def MSXgetID(type,index):
    """Retrieves the ID name of an object given its internal index number
    Arguments:
    type:
    MSX_SPECIES - 3 (for a chemical species)
    MSX_CONSTANT - 6 (for a reaction constant
    MSX_PARAMETER - 5 (for a reaction parameter)
    MSX_PATTERN - 7 (for a time pattern)
    maxlen: maxi number of characters that id can hold not counting null termination character"""
    type_ind = 100  # in case the type input is in text
    if type == 'MSX_SPECIES' or type == 3:
        type_ind = 3
    if type == 'MSX_CONSTANT' or type == 6:
        type_ind = 6
    if type == 'MSX_PARAMETER' or type == 5:
        type_ind = 5
    if type == 'MSX_PATTERN' or type == 7:
        type_ind = 7
    if type_ind == 100: raise Exception('unrecognized type')
    maxlen = 32
    id = ctypes.create_string_buffer(maxlen)
    ierr= _lib.MSXgetID(type_ind,ctypes.c_int(index),ctypes.byref(id),ctypes.c_int(maxlen-1))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return id.value

def MSXgetinitqual(type,ind,spe):
    """Retrieves the initial concentration of a particular chemical species assigned to a specific node
    or link of the pipe network.
    Arguments:
    type is type of object: MSX_NODE (0), MSX_LINK (1)
    ind is the internal sequence number (starting from 1) assigned to the node or link
    speicies is the sequence number of teh species (starting  from 1)"""
    type_ind = 100
    if type == 'MSX_NODE' or type == 0:
        type_ind = 0
    if type == 'MSX_LINK' or type == 1:
        type_ind = 1
    if type_ind == 100: raise Exception('unrecognized type')
    iniqual = ctypes.c_double()
    ierr= _lib.MSXgetinitqual(ctypes.c_int(type_ind),ctypes.c_int(ind),ctypes.c_int(spe),ctypes.byref(iniqual))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return iniqual.value

def MSXgetqual(type,ind,spe):
    """Retrieves a chemical species concentration at a given node or the average concentration along a link at the current simulation time step
    Arguments:
    type is type of object: MSX_NODE (0), MSX_LINK (1)
    ind is the internal sequence number (starting from 1) assigned to the node or link
    speicies is the sequence number of teh species (starting  from 1)
    concentrations expressed as: mass units per liter for bulk species and mass per unit area for surface species"""
    type_ind = 100
    if type == 'MSX_NODE' or type == 0:
        type_ind = 0
    if type == 'MSX_LINK' or type == 1:
        type_ind = 1
    if type_ind == 100: raise Exception('unrecognized type')
    qual = ctypes.c_double()
    ierr= _lib.MSXgetqual(ctypes.c_int(type_ind),ctypes.c_int(ind),ctypes.c_int(spe),ctypes.byref(qual))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return qual.value

def MSXgetconstant(ind):
    """Retrieves the value of a particular reaction constant
    Arguments:
    ind is the sequence number of the reaction constant (starting from 1) as it appeared in the MSX input file"""
    const = ctypes.c_double()
    ierr= _lib.MSXgetconstant(ind,ctypes.byref(const))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return const.value


def MSXgetparameter(type,ind,param_ind):
    """Retrieves the value of a particular reaction parameter for a give TANK or PIPE
    Arguments:
    type is the type of object: MSX_NODE (0) or MSX_LINK (1)
    ind is the internal sequence number(starting from 1) assigned to the node or link
    param is the sequence number of the parameter (starting from 1 as listed in the MSX input file)"""
    type_ind = 100  # in case type input is in text
    if type == 'MSX_NODE' or type == 0:
        type_ind = 0
    if type == 'MSX_LINK' or type == 1:
        type_ind = 1
    if type_ind == 100: raise Exception('unrecognized type')
    param = ctypes.c_double()
    ierr= _lib.MSXgetparameter(ctypes.c_int(type_ind),ctypes.c_int(ind),ctypes.c_int(param_ind),ctypes.byref(param))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return param.value

def MSXgetsource(node,spe):
    """Retrieves information on any external source of a particular chemical species assigned to a specific node of the pipe network
    Arguments:
    node is the internal sequence number (starting from 1) assigned to the node of interest
    species is the sequence number of the species of interest (starting from 1 as listed in the MSX input file)
    type is returned with the type of external source and will be one of the following pre-defined constants
    MSX_NOSOURCE (-1) no source; MSX_CONCEN (0) a concentration source; MSX_MASS (1) mass booster source;
    MSX_SETPOINT (2) setpoint source; MSX_FLOWPACED (3) flow paced source
    level is returned with the baseline concentration (or mass flow rate) of the source
    pat is returned with the index of the time pattern used to add variability to the source's baseline level (0 if no pattern defined for the source)"""
    level = ctypes.c_double()
    type = ctypes.c_int()
    pat = ctypes.c_int()
    ierr = _lib.MSXgetsource(ctypes.c_int(node),ctypes.c_int(spe),ctypes.byref(type),ctypes.byref(level),ctypes.byref(pat))
    if ierr!=0: raise MSXtoolkitError(ierr)
    src_out = [type.value,level.value,pat.value]
    return src_out

def MSXgetpatternlen(pat):
    """Retrieves the number of time periods within a SOURCE time pattern
    Arguments:
    pat is the internal sequence number (starting from 1) of the pattern as appears in the MSX input file"""
    len = ctypes.c_int()
    ierr = _lib.MSXgetpatternlen(pat,ctypes.byref(len))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return len.value

def MSXgetpatternvalue(pat,period):
    """Retrieves the multiplier at a specific time period for a given SOURCE time pattern
    Arguments:
    pat is the internal sequence number (starting from 1) of the pattern as appears in the MSX input file
    period is the index of the time period (starting from 1) whose multiplier is being sought
    value is the vlaue of teh pattern's multiplier in teh desired period"""
    val = ctypes.c_double()
    ierr = _lib.MSXgetpatternvalue(pat,period,ctypes.byref(val))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return val.value

def MSXgetcount(type):
    """Retrieves the number of objects of a specified type.
    Arguments:
    MSX_SPECIES - 3 (for a chemical species)
    MSX_CONSTANT - 6 (for a reaction constant
    MSX_PARAMETER - 5 (for a reaction parameter)
    MSX_PATTERN - 7 (for a time pattern)
    maxlen: maxi number of characters that id can hold not counting null termination character"""
    type_ind = 100  # in case the type input is in text
    if type == 'MSX_SPECIES' or type == 3:
        type_ind = 3
    if type == 'MSX_CONSTANT' or type == 6:
        type_ind = 6
    if type == 'MSX_PARAMETER' or type == 5:
        type_ind = 5
    if type == 'MSX_PATTERN' or type == 7:
        type_ind = 7
    if type_ind == 100: raise Exception('unrecognized type')
    count = ctypes.c_int()
    ierr= _lib.MSXgetcount(type_ind,ctypes.byref(count))
    if ierr!=0: raise MSXtoolkitError(ierr)
    return count.value

def MSXgetspecies(spe):
    """Retrieves the attributes of a chemical species given its internal index number.
        species is the sequence number of the species (starting from 1 as listed in teh MSX input file_
        type: MSX_BULK (defined as 0) and MSX_WALL (defined as 1)
        units: C_style character string array that is returned with the mass units that were defined for the species in question(hold max 15 characters)
        aTol returned with absolute concentration tolerance defined for the species
        rTol returned with the relative concentration tolerance defined for the species"""
    type_ind = ctypes.c_int()
    units = ctypes.create_string_buffer(15)
    aTol = ctypes.c_double()
    rTol = ctypes.c_double()
    ierr = _lib.MSXgetspecies(spe,ctypes.byref(type_ind),ctypes.byref(units),ctypes.byref(aTol),ctypes.byref(rTol))
    if ierr != 0: raise MSXtoolkitError(ierr)
    spe_out = [type_ind.value,units.value,aTol.value,rTol.value]
    return spe_out

def MSXgeterror(errcode,len=100):
    """returns the text for an error message given its error code
    arguments:
    code is the code number of an error condition generated by EPANET-MSX
    msg is a C-style string containing text of error message corresponding to error code
    len is the max number of charaters that msg can contain (at least 80)"""
    errmsg= ctypes.create_string_buffer(len)
    _lib.MSXgeterror(errcode,ctypes.byref(errmsg),len)
    return errmsg.value.decode()

#--------------set parameters-----------------------------------

def MSXsetconstant(ind,value):
    """assigns a new value to a specific reaction constant
    Arguments:
    ind is the sequence number of the reaction constant (starting from 1) as it appreaed in the MSX input file
    value is the new value to be assigned to the constant"""
    ierr= _lib.MSXsetconstant(ctypes.c_int(ind),ctypes.c_double(value))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXsetparameter(type,ind,param,value):
    """assigns a value to a particular reaction parameter for a given TANK or PIPE
    Arguments:
    type is the type of object: MSX_NODE (0) or MSX_LINK (1)
    ind is the internal sequence number(starting from 1) assigned to the node or link
    param is the sequence number of the parameter (starting from 1 as listed in the MSX input file"""
    type_ind = 100
    if type == 'MSX_NODE' or type == 0:
        type_ind = 0
    if type == 'MSX_LINK' or type == 1:
        type_ind = 1
    if type_ind == 100: raise Exception('unrecognized type')
    ierr= _lib.MSXsetparameter(ctypes.c_int(type_ind),ctypes.c_int(ind),ctypes.c_int(param),ctypes.c_double(value))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXsetinitqual(type,ind,spe,value):
    """Retrieves the initial concentration of a particular chemical species assigned to a specific node
    or link of the pipe network.
    Arguments:
    type is type of object: MSX_NODE (0), MSX_LINK (1)
    ind is the internal sequence number (starting from 1) assigned to the node or link
    speicies is the sequence number of teh species (starting  from 1)"""
    type_ind = 100
    if type == 'MSX_NODE' or type == 0:
        type_ind = 0
    if type == 'MSX_LINK' or type == 1:
        type_ind = 1
    if type_ind == 100: raise Exception('unrecognized type')
    ierr= _lib.MSXsetinitqual(ctypes.c_int(type_ind),ctypes.c_int(ind),ctypes.c_int(spe),ctypes.c_double(value))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXsetsource(node,spe,type_n,level,pat):
    """sets the attributes of an external source of a particular chemical species in a specific node of the pipe network
    Arguments:
    node is the internal sequence number (starting from 1) assigned to the node of interest
    species is the sequence number of the species of interest (starting from 1 as listed in the MSX input file)
    type is returned with the type of exteernal source and will be one of the following pre-defined constants
    MSX_NOSOURCE (-1) no source; MSX_CONCEN (0) a concentration source; MSX_MASS (1) mass booster source;
    MSX_SETPOINT (2) setpoint source; MSX_FLOWPACED (3) flow paced source
    level is the baseline concentration (or mass flow rate) of the source
    pat is the index of the time pattern used to add variability to the source's baseline level (0 if no pattern defined for the source)"""
    type_ind = 100
    if type_n == 'MSX_NOSOURCE' or type_n == -1:
        type_ind = -1
    if type_n == 'MSX_CONCEN' or type_n == 0:
        type_ind = 0
    if type_n == 'MSX_MASS' or type_n == 1:
        type_ind = 1
    if type_n == 'MSX_SETPOINT' or type_n == 2:
        type_ind = 2
    if type_n == 'MSX_FLOWPACED' or type_n == 3:
        type_ind = 3
    if type_ind == 100: raise Exception('unrecognized type')
    ierr= _lib.MSXsetsource(ctypes.c_int(node),ctypes.c_int(spe),ctypes.c_int(type_ind),ctypes.c_double(level),ctypes.c_int(pat))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXsetpattern(pat,mult):
    """assigns a new set of multipliers to a given MSX SOURCE time pattern
    Arguments:
    pat is the internal sequence number (starting from 1) of the pattern as appears in the MSX input file
    mult is an array of multiplier values to replace those preciously used by the pattern
    len is the number of entries in mult"""
    length = len(mult)
    cfactors_type= ctypes.c_double*length
    cfactors = cfactors_type()
    for i in range(length):
       cfactors[i]= float(mult[i])
    ierr= _lib.MSXsetpattern(ctypes.c_int(pat),cfactors,ctypes.c_int(length))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXsetpatternvalue(pat,period,value):
    """Sets the multiplier factor for a specific period within a SOURCE time pattern.
    Arguments:
       index: time pattern index
       period: period within time pattern
       value:  multiplier factor for the period"""
    ierr= _lib.MSXsetpatternvalue(ctypes.c_int(pat),ctypes.c_int(period),ctypes.c_double(value))
    if ierr!=0: raise MSXtoolkitError(ierr)

def MSXaddpattern(patternid):
    """Adds a new, empty MSX source time pattern to an MSX project.
    Arguments:
      pattern id: c-string name of pattern"""
    ierr=_lib.MSXaddpattern(ctypes.c_char_p(patternid.encode()))
    if ierr!=0: raise MSXtoolkitError(ierr)

#---------------error messages-------------------------------------------------------------------------
class MSXtoolkitError(Exception):
    def __init__(self, ierr):
      self.warning= ierr < 100
      self.args= (ierr,)
      self.message= MSXgeterror(ierr)
      if self.message=='' and ierr!=0:
         self.message='MSXtoolkit Undocumented Error '+str(ierr)+': look at text.h in epanet sources'
    def __str__(self):
      return self.message

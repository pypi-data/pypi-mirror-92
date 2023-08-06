"""
qutiepy.py
==========================
The main file containing the core components of QutiePy
"""
import numpy as np
import scipy.linalg as sp
import random




class register:
    """
    N-bit quantum register. The initial state is (1+0j)|0>.
    
    Parameters
    ----------
    NBits : int
        Size of the register in bits.

    Attributes
    ----------
    NBits : int
        Number of bits in the register.
    
    NStates : int
        Number of states the register can occupy (2^NBits).
    
    amps : list
        The complex probability amplitudes of each state of the register.

    """
    def __init__(self, NBits):
        _checkNBits(NBits)
        self.NBits = NBits
        self.NStates = 2 ** NBits
        self.amps = np.zeros(self.NStates, dtype=np.dtype(complex))
        self.amps[0] = 1 + 0j
    
    def probabilities(self):
        """ Return the probability associated with observing each state. 
        
        Returns
        ----------
        probabilities : numpy array
            The probabilities p(X=x_i) of observing each state.
        """
        return np.array([abs(i)**2 for i in self.amps])
    
    def observe(self, collapseStates=True):
        """ 'Observe' the register and return an integer representation of the
            observed state according to the probability amplitudes.

            If collapseStates=True, adjust the amplitudes to reflect the collapsed
            state.
            
            Returns
            ----------
            state : int
                The observed state.
        """
        probs = self.probabilities()
        choice = random.choices(range(self.NStates), probs)[0]

        if collapseStates:
            amps = [0]*self.NStates
            amps[choice] = 1
            self.setAmps(amps)
        
        return choice
    
    def __str__(self):
        stri = ""
        for state, amp in enumerate(self.amps):
            stri = stri + f" {amp:.3f}".rjust(15) + " |" + str(state).ljust(2) + "> +\r\n"
        return stri.rstrip("+\r\n")
    
    def prod(self, B):
        """ Return the tensor product of self and B, 'Joining' two registers 
            into a single larger register with self at the MSB and 'B' at the LSB.
            
            Parameters
            ----------
            B : register
                The register to be appended to self.
            
            Returns
            ----------
            result : register
                The resulting joined register.
                
            See Also
            ----------
            prod : Equivalent function
        """
        result = register(self.NBits + B.NBits)
        result.amps = np.kron(self.amps, B.amps)    
        return result
    
    def bloch(self, eps=1e-12):
        """ Return the angles theta and phi used in the Bloch sphere representation 
        of a single qubit register (eps is used to avoid infinite and NaN results,
        set to 0 to disable).
        
        Returns
        ----------
        theta : float
            The angle theta = 2*arccos(amps[0]).
        
        phi : float
            The angle phi = Ln[(amps[1]+eps)/(sin(theta/2)+eps)].
        
        """
        if self.NBits != 1:
            raise ValueError("bloch() can only be called on 1-bit registers.")

        theta = 2 * np.arccos(self.amps[0])
        phi = np.real(np.log((self.amps[1]+eps)/(np.sin(theta/2)+eps))/1j)   # cast as float here?

        return theta, phi
    
    def density(self):
        """ Return the density matrix of the register. 
        
        Returns
        ----------
        density : numpy array
            The density matrix.
        """
        density = np.outer(self.amps, np.asmatrix(self.amps).H)
        
        return np.real(density)
    
    def reducedPurities(self):
        """ Return the reduced purity of each bit of the register, i.e.:
            Tr[Tr_i(D)^2]
            where D is the full density matrix of the register and Tr_i is 
            the partial trace over the subspace of bit index 'i'.
            
            Returns
            ----------
            purities : numpy array
                The reduced purity of each qubit in the register.
        """
        d = self.density()
        purities = []
        idxs = list(range(self.NBits))

        for i in idxs:
            theseidxs = idxs.copy()
            theseidxs.remove(i)
            pt = _partial_trace(d, theseidxs , [2]*(self.NBits), True)
            pt2 = np.matmul(pt,pt)
            purities.append(round(np.trace(pt2),8))
            # round used to reduce precision and remove small errors


        return np.array(purities)
    
    def setAmps(self, amps):
        """ Manually set the qubit probability amplitudes in-place, ensuring they remain properly normalised. 
        
        Parameters
        ----------
        amps : iterable
            The relative complex amplitudes to be applied to the register with normalisation.
        """
        if len(amps) != self.NStates:
            raise ValueError("Length of iterable 'amps' must be equal to NStates.")
        
        probs = np.array([abs(i)**2 for i in amps])
        self.amps = np.array(amps,  dtype=np.dtype(complex)) / sum(probs)**0.5



def prod(regA, regB):
    """ 'Join' two registers into a single larger register with regA at the MSB and regB at the LSB 
    by performing the tensor product between their state vectors \|A>\|B> = \|AB>. 
    
    Parameters
    ----------
    regA : register
        The register to be placed at the MSB.
    
    regB : register
        The register to be placed at the LSB.
    
    Returns
    ----------
    result : register
        The resulting joined register.
        
    See Also
    ----------
    register.prod : Equivalent class method.
    """
    result = register(regA.NBits + regB.NBits)
    result.amps = np.kron(regA.amps, regB.amps)  
    return result


def _partial_trace(rho, keep, dims, optimize=False):
    """Calculate the partial trace (Thanks to slek120 on StackExchange)

    ρ_a = Tr_b(ρ)

    Parameters
    ----------
    ρ : 2D array
        Matrix to trace
    keep : array
        An array of indices of the spaces to keep after
        being traced. For instance, if the space is
        A x B x C x D and we want to trace out B and D,
        keep = [0,2]
    dims : array
        An array of the dimensions of each space.
        For instance, if the space is A x B x C x D,
        dims = [dim_A, dim_B, dim_C, dim_D]

    Returns
    -------
    ρ_a : 2D array
        Traced matrix
    """
    keep = np.asarray(keep)
    dims = np.asarray(dims)
    Ndim = dims.size
    Nkeep = np.prod(dims[keep])

    idx1 = [i for i in range(Ndim)]
    idx2 = [Ndim+i if i in keep else i for i in range(Ndim)]
    rho_a = rho.reshape(np.tile(dims,2))
    rho_a = np.einsum(rho_a, idx1+idx2, optimize=optimize)
    return rho_a.reshape(Nkeep, Nkeep)

class genericGate:
    """
    Base class for callable quantum logic gates.
    
    Parameters
    ----------
    NBits : int
        Size of the registers that the gate will take as input/output.

    Attributes
    ----------
    NBits : int
        Number of bits that the gate takes as input/output.
    
    matrix : 2D numpy array
        The 2^NBits by 2^NBits matrix representation of the gate.

    """
    def __init__(self, NBits):
        _checkNBits(NBits)
        self.NBits = NBits
        self.matrix = np.identity(2 ** NBits)
    
    def __call__(self, arg):
        if issubclass(type(arg), genericGate):
            out = genericGate(self.NBits + arg.NBits)
            out.matrix = np.matmul(self.matrix, arg.matrix)
            return out

        elif type(arg) == register:
            result = register(arg.NBits)
            result.amps = np.matmul(self.matrix, arg.amps)
            return result
        
        else:
            raise TypeError("Gates can only be called on gates or registers! Got type: " +  str(type(arg)))
    
    def __str__(self):
        stri = str(self.NBits) + "-bit " + type(self).__name__ + " Gate, Matrix:\n\r"
        stri = stri + self.matrix.__str__()
        return stri

class hadamard(genericGate):
    """ A callable hadamard gate object. 
    
    Parameters
    ----------
    NBits : int
        Number of bits that the gate takes as input/output.
    
    """
    def __init__(self, NBits):
        super(hadamard, self).__init__(NBits)
        self.matrix = sp.hadamard(2 ** NBits) * (2**(-0.5*(NBits)))

class phaseShift(genericGate):
    """ A callable phase-shift gate object. 
    
    Parameters
    ----------
    NBits : int
        Number of bits that the gate takes as input/output.
    
    phi : float
        The phase angle through which to shift the amplitudes.
    """
    def __init__(self, NBits, phi):
        super(phaseShift, self).__init__(NBits)
        singleMatrix = np.array([[1,0],[0,np.exp(phi * 1j)]])
        self.matrix = _toNBitMatrix(singleMatrix, NBits)

class pauliX(genericGate):
    """ A callable Pauli-X gate object. 
    
    Parameters
    ----------
    NBits : int
        Number of bits that the gate takes as input/output.
    """
    def __init__(self, NBits):
        super(pauliX, self).__init__(NBits)
        singleMatrix = np.array([[0,1],[1,0]])    
        self.matrix = _toNBitMatrix(singleMatrix, NBits)

class pauliY(genericGate):
    """ A callable Pauli-Y gate object. 
    
    Parameters
    ----------
    NBits : int
        Number of bits that the gate takes as input/output.
    """
    def __init__(self, NBits):
        super(pauliY, self).__init__(NBits)
        singleMatrix = np.array([[0,-1j],[1j,0]])    
        self.matrix = _toNBitMatrix(singleMatrix, NBits) 

class pauliZ(phaseShift):
    """ A callable Pauli-Z gate object. 
    
    Parameters
    ----------
    NBits : int
        Number of bits that the gate takes as input/output.
    """
    def __init__(self, NBits):
        super(pauliZ, self).__init__(NBits, np.pi)

class cNot(genericGate):
    """ A callable CNOT gate object. 
    
    The first bit (LSB) in the register on which this gate is called is the control bit.
    """ 
    
    def __init__(self):     # (first bit is the control bit)
        super(cNot, self).__init__(2)   
        self.matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])

class ccNot(genericGate):
    """ A callable CCNOT (Toffoli) gate object.
    
    The first two bits (LSBs) in the register on which this gate is called are the control bits. 
    """
    def __init__(self):
        super(ccNot, self).__init__(3)
        self.matrix = np.eye(8)
        self.matrix[6:8, 6:8] = np.array([[0,1],[1,0]])

def _checkNBits(NBits):
    """ Validate the NBits input. """
    if NBits < 1:
        raise ValueError("NBits must be a positive integer!")
    
    if type(NBits) != int:
        raise TypeError("NBits must be a positive integer!")

def _toNBitMatrix(m, NBits, skipBits=[]):   # add ability to skip bits???
    """ Take a single-bit matrix of a gate and return the NBit equivalent matrix """
    m0 = m
    mOut = m
    for i in range(NBits - 1):
        mOut = np.kron(mOut, m0)
    
    return mOut

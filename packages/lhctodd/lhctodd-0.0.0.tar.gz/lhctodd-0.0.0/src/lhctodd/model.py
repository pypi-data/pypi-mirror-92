from .tools import __data_path__
from .tools import dd_format
from scipy import interpolate

import lmdb
import pickle
import matplotlib.pyplot as plt


class DD:
    # Direct Detection measurements
    def __init__(self, limit_id=None, pattern=None, arxiv=None):
        self._data = None
        self._env = lmdb.open(str( __data_path__ / f"darkmatter-data"), readonly=True)
        with self._env.begin() as txn:
            if limit_id is not None:
                data = txn.get(f"{limit_id:08}".encode("ascii"))
                self._data = pickle.loads(data)
            else:
                for key, _ in txn.cursor():
                    raw = txn.get(key)
                    data = pickle.loads(raw)
                    if pattern is not None:
                        if pattern in data.__dict__.values():
                            self._data = data
                            break
                    if arxiv is not None:
                        if arxiv in data.cite:
                            self._data = data
                            break
        self._env.close()

        assert self._data is not None
        self._limit = self._data.get_limit()
        self.name = self._data.name
        self.type = self._data.type
        self.cite = "https://arxiv.org/abs/{}".format(self._data.cite)
        self._func = interpolate.interp1d(
            self._limit[:,0],
            self._limit[:,1],
            fill_value="extrapolate"
        )

    def sigma(self, mass=100):
        return self._func(mass)

    def data(self):
        return self._data.get_limit()

    def to_pandas(self):
        return pd.DataFrame(
            self._data.get_limit(),
            columns=["mass", "sigma"]
        )
    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        ax.plot(
            self._limit[:,0],
            self._limit[:,1],
            label= self._data.name
        )

        ax.set_xlabel("$m_{\chi}$")
        ax.set_ylabel(
            "{model} DM-nucleon cross-section (cm$^2$)".format(
                model=self._data.type
            )
        )
        ax.set_xscale("log")
        ax.set_yscale("log")


class sim_model:
    # simplified model
    def __init__(self, g_chi=1.0, g_quark=0.25, g_lepton=0.0, label=None):
        self.med_mass = None
        self.chi_mass = None
        self.g_chi = g_chi
        self.g_quark = g_quark
        self.g_lepton = g_lepton
        self.limit = None
        self.type = ""
        self.label = label

    def from_csv(self, filename, delimiter=","):
        print("filename : ", filename, delimiter)
        my_data = np.genfromtxt(filename, delimiter=delimiter)
        self.med_mass = my_data[:,0] # mediator
        self.chi_mass = my_data[:,1] # darkmatter
        return np.vstack([
            self.sigma(self.med_mass, self.chi_mass),
            self.chi_mass
        ]).T

    def sigma(self, med_mass, chi_mass):
        raise NotImplementedError("sigma not implemented!")

    def plot(self, ax=None):
        if ax is None:
            ax = plt.gca()

        ax.plot(
            self.chi_mass,
            self.sigma(self.med_mass, self.chi_mass),
            label= self.label
        )

        ax.set_xlabel("$m_{\chi}$")
        ax.set_ylabel(
            "{model} DM-nucleon cross-section (cm$^2$)".format(
                model=self.type
            )
        )
        ax.set_xscale("log")
        ax.set_yscale("log")


class SD(sim_model):
    """Translate LHC 2D limits on Axial-Vector mediator onto limit on DM-Nucleon cross section
    The values of the couplings should correspond to the model used to extract your limits

    Parameters
    ----------
    g_chi: coupling value to Dark Matter candidate $g_{\chi}$
    g_quark: coupling value to quarks $g_q$
    g_lepton: coupling value to leptons $g_\ell$
    label: used to label the curve when plot function is called

    Examples
    --------
    from a CSV file that contains the observed 2D limit
    $(m_{med}, m_{\chi})$, with $m_{med}$ is the mass of
    the mediator and $m_\chi$ is the one for the Dark Matter
    >>> import lhctodd as dd
    >>> model = dd.Axial(g_chi=1.0, g_qaurk=0.25)
    >>> model.from_csv("some-limit-from-lhc.csv")
    >>> model.plot()

    All in one line
    >>> dm_mass, limit_sigma = dd.Axial(g_chi=1.0, g_qaurk=0.25).from_csv("some-limit-from-lhc.csv")
    >>> plt.plot(dm_mass, limit_sigma)
    """
    def __init__(self, g_chi=1.0, g_quark=0.25, g_lepton=0.0, label=None):
        super().__init__(g_chi, g_quark, g_lepton, label)
        self.neutron_mass = 0.939

    def sigma(self, med_mass, chi_mass):
        rat = self.neutron_mass * chi_mass / (chi_mass + self.neutron_mass)
        sigma = 2.4e-42
        sigma *= np.power(self.g_quark*self.g_chi/0.25, 2)
        sigma *= np.power(1000./med_mass, 4)
        sigma *= np.power(rat,2)
        return sigma


class SI(sim_model):
    """Translate LHC 2D limits on Vector or Scalar mediators onto limit on DM-Nucleon cross section
    The values of the couplings should correspond to the model used to extract your limits

    Parameters
    ----------
    g_chi: coupling value to Dark Matter candidate $g_{\chi}$
    g_quark: coupling value to quarks $g_q$
    g_lepton: coupling value to leptons $g_\ell$
    label: used to label the curve when plot function is called

    Examples
    --------
    from a CSV file that contains the observed 2D limit
    $(m_{med}, m_{\chi})$, with $m_{med}$ is the mass of
    the mediator and $m_\chi$ is the one for the Dark Matter
    >>> import lhctodd as dd
    >>> model = dd.Vector(g_chi=1.0, g_qaurk=0.25)
    >>> model.from_csv("some-limit-from-lhc.csv")
    >>> model.plot()

    All in one line
    >>> dm_mass, limit_sigma = dd.Vector(g_chi=1.0, g_qaurk=0.25).from_csv("some-limit-from-lhc.csv")
    >>> plt.plot(dm_mass, limit_sigma)
    """

    def __init__(self, g_chi=1.0, g_quark=0.25, g_lepton=0.0, label=None):
        super().__init__(g_chi, g_quark, g_lepton, label)
        self.neutron_mass = 0.939

    def sigma(self, med_mass, chi_mass):
        rat = self.neutron_mass * chi_mass / (chi_mass + self.neutron_mass)
        sigma = 6.9e-41
        sigma *= np.power(self.g_quark*self.g_chi/0.25, 2)
        sigma *= np.power(1000./med_mass, 4)
        sigma *= np.power(rat,2)
        return sigma

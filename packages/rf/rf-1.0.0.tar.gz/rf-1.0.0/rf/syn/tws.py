# Copyright 2019 Tom Eulenfeld, MIT license

"""
Wrapper arround telewavesim package utilizing the matrix propagator approach.

See Kennet1983, Thomson1997, BostockTrehu2012.
"""
from pkg_resources import resource_filename
import numpy as np

from rf.util import DEG2KM

try:
    import telewavesim.utils as _tws
    from telewavesim.utils import Model as _TWSModel
except ImportError as error:
    msg = 'telewavesim import error. rf.synthetic.tws module not working.'
    raise ImportError(msg) from error


def load_model(fname, encoding=None):
    """
    Reads model parameters from file and returns a Model object.

    """
    if fname in ['Audet2016', 'Porter2011', 'SKS']:
        fname = resource_filename('telewavesim',
                                  'examples/models/model_%s.txt' % fname)
    values = np.genfromtxt(fname, dtype=None, encoding=encoding)
    return TWSModel(*zip(*values))

class TWSModel(_TWSModel):

    def calc_ttime(self, slowness, wvtype='P'):
        hslow = slowness / DEG2KM  # convert to horizontal slowness (s/km)
        return _tws.calc_ttime(self, hslow, wvtype=wvtype)

    def synthetic_coordinates(self, npts, delta, station, event,
                              **kwargs):
        slowness, back_azimuth = None, None
        return self.synthetic(npts, delta, slowness, back_azimuth, **kwargs)

    def synthetic(self, npts, delta,
                  slowness, back_azimuth=0, wvtype='P',
                  depth=None, c=1.5, rhof=1027,
                  tshift=0, rtype='tf', rotate='ZRT'
                  ):
        # set metadata of stream and transfer function
        # components etc

        # add tests
        hslow = slowness / DEG2KM  # convert to horizontal slowness (s/km)
        stream = _tws.run_plane(self, hslow, npts, delta, baz=back_azimuth,
                                wvtype=wvtype, obs=depth is not None,
                                dp=depth, c=c, rhof=rhof)
#        if rotate.upper() == 'PVH':
#            stream = _tws.rotate_zrt_pvh(stream[0], stream[1], stream[2],
#                                         hslow, vp=self.vp[0], vs=self.vs[0])
        if rtype == 'tf':
            stream = _tws.tf_from_xyz(stream, pvh=rotate.upper() == 'PVH',
                                      vp=self.vp[0], vs=self.vs[0])
        if tshift != 0:
            for tr in stream:
                n = int(round(tshift/delta))
                tr.data = np.roll(tr.data, n)
                tr.data[:n] = 0
        return stream

    def __repr__(self):
        s = ('TWSModel(' + ', '.join(
                 '{0}={{0.{0}!r}}'.format(k)
                 for k in 'thickn rho vp vs isoflg ani tr pl'.split()) + ')')
        return s.format(self)


def test():
    from pkg_resources import resource_filename
    fname = resource_filename('telewavesim',
                              'examples/models/model_Porter2011.txt')
    model = load_model(fname)
    return model
from pysimmods.generator.pvsystemsim.presets import pv_preset
from pysimmods.consumer.hvacsim.presets import hvac_preset
from pysimmods.generator.chplpgsystemsim.presets import chp_presets
from pysimmods.buffer.batterysim.presets import battery_presets


def get_presets(model, p_peak_mw, **kwargs):
    """Return presets for *model* with *p_peak_mw*.

    The presets are taken from the pysimmods package itself.

    """

    if model == "PV":
        params, inits = pv_preset(p_peak_kw=p_peak_mw * 1e3, **kwargs)
        params["sn_mva"] = params["inverter"]["sn_kva"] * 1e-3
        return params, inits
    elif model == "HVAC":
        return hvac_preset(pn_max_kw=p_peak_mw * 1e3, **kwargs)
    elif model == "CHP":
        return chp_presets(p_kw=p_peak_mw * 1e3, **kwargs)
    elif model == "BAT":
        return battery_presets(pn_max_kw=p_peak_mw * 1e3)
    else:
        raise ValueError(f"Model {model} is unknown.")

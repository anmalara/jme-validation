from bamboo import treefunctions as op
from bamboo.plots import Plot
from bamboo.plots import EquidistantBinning as EqBin
from src.binnings import eta_binning, pt_binning, response_pt_binning

def muonPlots(muons, sel, sel_tag, maxMuons = 4):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_Muon_nMuons", op.rng_len(muons), sel, EqBin(15, 0., 15.),xTitle = "Number of muons"))
    
    #### do a for loop through all Muons
    for i in range(maxMuons):
        plots.append(Plot.make1D(f"{sel_tag}_Muon{i+1}_pt", muons[i].pt, sel, EqBin(20, 0., 500.), xTitle=f"muon_{{{i+1}}} p_{{T}} [GeV]"))
        plots.append(Plot.make1D(f"{sel_tag}_Muon{i+1}_eta", muons[i].eta, sel, EqBin(20, -2.5, 2.5), xTitle=f"muon_{{{i+1}}} #eta"))
        plots.append(Plot.make1D(f"{sel_tag}_Muon{i+1}_phi", muons[i].phi, sel, EqBin(20, -2.5, 2.5), xTitle=f"muon_{{{i+1}}} #phi"))
 
    return plots


def electronPlots(electrons, sel, sel_tag, maxElectrons = 4):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_Electron_nElectrons", op.rng_len(electrons), sel, EqBin(15, 0., 15.), xTitle=f"Number of Electrons"))
    
    #### do a for loop through all Electrons
    for i in range(maxElectrons):
        plots.append(Plot.make1D(f"{sel_tag}_Electron{i+1}_pt", electrons[i].pt, sel, EqBin(20, 0., 500.), xTitle=f"electron_{{{i+1}}} p_{{T}} [GeV]"))
        plots.append(Plot.make1D(f"{sel_tag}_Electron{i+1}_eta", electrons[i].eta, sel, EqBin(20, -2.5, 2.5), xTitle=f"electron_{{{i+1}}} #eta"))
        plots.append(Plot.make1D(f"{sel_tag}_Electron{i+1}_phi", electrons[i].phi, sel, EqBin(20, -2.5, 2.5), xTitle=f"electron_{{{i+1}}} #phi"))
 
    return plots


def AK4jetPlots(jets, sel, sel_tag, maxJets=4):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_nJets",op.rng_len(jets),sel,EqBin(15,0.,15.), xTitle=f"Number of Jets"))
    #### do a for loop through all Jets
    for i in range(maxJets):
        plots.append(Plot.make1D(f"{sel_tag}_Jet{i+1}_pt", jets[i].pt, sel, EqBin(20, 0., 500.), xTitle=f"jet_{{{i+1}}} p_{{T}} [GeV]"))
        plots.append(Plot.make1D(f"{sel_tag}_Jet{i+1}_eta", jets[i].eta, sel, EqBin(100, -5., 5.), xTitle=f"jet_{{{i+1}}} #eta"))
        plots.append(Plot.make1D(f"{sel_tag}_Jet{i+1}_phi", jets[i].phi, sel, EqBin(63, -3.5, 3.5), xTitle=f"jet_{{{i+1}}} #phi"))


    chEmEF = op.map(jets, lambda j: j.chEmEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_chEmEF",chEmEF,sel,EqBin(20,0.,1.), xTitle=f"chEmEF"))

    chHEF = op.map(jets, lambda j: j.chHEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_chHEF",chHEF,sel,EqBin(20,0.,1.), xTitle=f"chHEF"))
    
    hfEmEF = op.map(jets, lambda j: j.hfEmEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_hfEmEF",hfEmEF,sel,EqBin(20,0.,1.), xTitle=f"hfEmEF"))

    hfHEF = op.map(jets, lambda j: j.hfHEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_hfHEF",hfHEF,sel,EqBin(20,0.,1.), xTitle=f"hfHEF"))

    muEF = op.map(jets, lambda j: j.muEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_muEF",muEF,sel,EqBin(20,0.,1.), xTitle=f"muEF"))

    neEmEF = op.map(jets, lambda j: j.neEmEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_neEmEF",neEmEF,sel,EqBin(20,0.,1.), xTitle=f"neEmEF"))

    neHEF = op.map(jets, lambda j: j.neHEF)
    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_neHEF",neHEF,sel,EqBin(20,0.,1.), xTitle=f"neHEF"))


    return plots



def ZbosonPlots(Zboson, sel, sel_tag):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_Zboson_mass",Zboson.M(),sel,EqBin(30,0.,200.),xTitle="m_{ll} [GeV]"))

    plots.append(Plot.make1D(f"{sel_tag}_Zboson_pt",Zboson.pt(),sel,EqBin(30,0.,200.),xTitle="Z boson p_{T} [GeV]"))

    return plots


def effPurityPlots(jet, sel, sel_tag, tree):
    plots = []
    
    genjets = op.select(tree.GenJet, lambda j: j.pt>20)
    
    deltaRs = op.map(jet, lambda j: op.deltaR(j.p4,j.genJet.p4))
    plots.append(Plot.make1D(f"{sel_tag}_deltaR", deltaRs,sel,EqBin(300,0.,3.),xTitle = "#Delta R (recojet, genjet)"))


    ### eff and purity bins of eta vs pt
    for etatag,etabin in eta_binning.items():
        etajets = op.select(jet, lambda j: op.AND(
            op.abs(j.genJet.eta) > etabin[0],
            op.abs(j.genJet.eta) < etabin[1]
        ))

        etagenjets = op.select(genjets, lambda j:op.AND(
            op.abs(j.eta) > etabin[0],
            op.abs(j.eta) < etabin[1]
        ))

        genjetpt = op.map(etajets, lambda j: j.genJet.pt)
        plots.append(Plot.make1D(f"{sel_tag}_{etatag}_genpt", genjetpt,sel,EqBin(200,0.,1000.),xTitle = "genjet p_{T} [GeV] "))
        recojetpt = op.map(etajets, lambda j: j.pt)
        plots.append(Plot.make1D(f"{sel_tag}_{etatag}_recopt", recojetpt,sel,EqBin(200,0.,1000.),xTitle = "recojet p_{T} [GeV] "))

        unmatchedgenjetpt = op.map(etagenjets, lambda j: j.pt)
        plots.append(Plot.make1D(f"{sel_tag}_{etatag}_unmatchedgenpt", unmatchedgenjetpt,sel,EqBin(200,0.,1000.),xTitle = "all genjet p_{T} [GeV] "))

        ####### vs NPU for the leading jet in bins of pT
        for pttag, ptbin in pt_binning.items():
            npujets = op.select(etajets, lambda j: op.AND(
                j.genJet.pt > ptbin[0],
                j.genJet.pt < ptbin[1]
            ))

            npvs = op.map(npujets, lambda j: tree.PV.npvsGood)
            plots.append(Plot.make1D(f"{sel_tag}_{etatag}_{pttag}_goodnpvs", npvs,sel,EqBin(100,0.,100.),xTitle = "Number of good PVs"))
            npus = op.map(npujets, lambda j: tree.Pileup.nTrueInt)
            plots.append(Plot.make1D(f"{sel_tag}_{etatag}_{pttag}_nTrueInt", npus,sel,EqBin(100,0.,100.),xTitle = "Number of true interactions"))
            
    return plots



def responsePlots(jets, sel, sel_tag, tree):
    plots = []

    deltaRs = op.map(jets, lambda j: op.deltaR(j.p4,j.genJet.p4))
    plots.append(Plot.make1D(f"{sel_tag}_deltaR", deltaRs,sel,EqBin(300,0.,3.),xTitle = "#Delta R (recojet, genjet)"))

    plots.append(Plot.make1D(f"{sel_tag}_njets", op.rng_len(jets),sel,EqBin(10,0.,10.),xTitle = "Number of jets"))

    for etatag,etabin in eta_binning.items():
        for pttag,ptbin in response_pt_binning.items():
            etaptjets = op.select(jets, lambda j: op.AND(
                op.abs(j.eta) > etabin[0],
                op.abs(j.eta) < etabin[1],
                j.genJet.pt > ptbin[0],
                j.genJet.pt < ptbin[1]
            ))
            response = op.map(etaptjets, lambda j: j.pt/j.genJet.pt)
            plots.append(Plot.make1D(f"{sel_tag}_{etatag}_{pttag}", response,sel,EqBin(100,0.,3.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))

    return plots
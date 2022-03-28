# This script fits the Z peak in given input TH1D histograms
# It should be run inside a CMSSW environment
# It uses a gaussian fit for signal with CMSSShape for background
# Requires RooCMSShape.cc and RooCMSShape.h in the same dir

import ROOT
ROOT.gSystem.Load('')
ROOT.gInterpreter.Declare('#include "RooCMSShape.cc"')

def do_z_fit(in_hist,in_hist_name):

    print("\n\n-----------------------",in_hist_name,"-----------------------\n\n")
    # Variable for the z mass
    Z_mass  = ROOT.RooRealVar("Z_mass","Z mass", 60, 120, "GeV")

    # The input histo
    roo_hist = ROOT.RooDataHist("histo", "histo", ROOT.RooArgList(Z_mass), ROOT.RooFit.Import(in_hist))

    # Params for gauss
    if "ssz" in in_hist_name:
        sigma_start = 4.0
        sigma_min   = 4.0
        sigma_max   = 7.0
        if "BH_BL" in in_hist_name: 
            sigma_start = 4.0
            sigma_min   = 4.0
            sigma_max   = 6.0
        if "EM_BL" in in_hist_name: 
            sigma_start = 6.0
            sigma_min   = 5.0
            sigma_max   = 7.0
    elif "osz" in in_hist_name:
        sigma_start = 1.0
        sigma_min = 0.1
        sigma_max = 6.0
    else:
        raise Exception

    # Params for norm
    nsig_min = 0.0; nbkg_min = 0.0; nsig_max = 0.0; nbkg_max = 0.0; nsig_start = 0.0; nbkg_start = 0.0;
    if "ssz" in in_hist_name:
        nsig_start = 50.0
        nbkg_start = 50.0
        nsig_min = 0.0
        nbkg_min = 0.0
        nsig_max = 1000.0
        nbkg_max = 1000.0
    elif "osz" in in_hist_name:
        nsig_start = 100000.0
        nbkg_start = 100000.0
        nsig_min = 1000.0
        nbkg_min = 1000.0
        nsig_max = 10000000.0
        nbkg_max = 10000000.0
    else:
        raise Exception

    #Parameters for gaus fit ("name", "name", initial_value, lower_limit, upper_limit)
    #gauss1_mean  = ROOT.RooRealVar("mean", "mean of gaussians", 91.0, 90.0, 100.0)
    gauss1_mean  = ROOT.RooRealVar("mean", "mean of gaussians", 85.0, 78.0, 94.0)
    #gauss1_sigma = ROOT.RooRealVar("sigma", "sigma", 3.0, 3.0, 30.0)
    #gauss1_sigma = ROOT.RooRealVar("sigma", "sigma", 3.0, 3.0, 40.0)
    #gauss1_sigma = ROOT.RooRealVar("sigma", "sigma", 5.0, 4.0, 10.0)
    gauss1_sigma = ROOT.RooRealVar("sigma", "sigma", sigma_start, sigma_min, sigma_max)
    gauss1_pdf   = ROOT.RooGaussian("gaus1", "gaussian1", Z_mass, gauss1_mean, gauss1_sigma)

    #Parameters for CMSShape fit ("name", "name", initial_value, lower_limit, upper_limit)  
    cmsshape_al      = ROOT.RooRealVar("al", "al", 79.0, 70.0, 100.0)
    #cmsshape_al      = ROOT.RooRealVar("al", "al", 150.0, 110.0, 300.0)
    cmsshape_beta    = ROOT.RooRealVar("beta", "beta", 0.005, 0.0, 3.0)
    cmsshape_lambda0 = ROOT.RooRealVar("lambda", "slope", 90.0, 60.0, 120.0)
    cmsshape_gamma   = ROOT.RooRealVar("gamma", "gamma", 0.2, 0.0, 2.0)
    cmsshape_pdf     = ROOT.RooCMSShape("bkg", "CMSModel", Z_mass, cmsshape_al, cmsshape_beta, cmsshape_gamma, cmsshape_lambda0)


    # Add the PDFs
    nsig    = ROOT.RooRealVar("nsig", "n sgl events", nsig_start, nsig_min, nsig_max)
    nbkg    = ROOT.RooRealVar("nbkg", "n bkg events", nbkg_start, nbkg_min, nbkg_max)
    model   = ROOT.RooAddPdf("model", "conv+bkg", ROOT.RooArgList(gauss1_pdf,cmsshape_pdf), ROOT.RooArgList(nsig, nbkg))
    #model   = ROOT.RooAddPdf("model", "conv+bkg", ROOT.RooArgList(gauss1_pdf), ROOT.RooArgList(nsig)) # No background
    #model   = ROOT.RooAddPdf("model", "conv+bkg", ROOT.RooArgList(cmsshape_pdf), ROOT.RooArgList(nbkg)) # No signal
    nsig_initial = nsig.getVal()

    # Run the fit
    model.fitTo(roo_hist, ROOT.RooFit.SumW2Error(True), ROOT.RooFit.Minos(True), ROOT.RooFit.Range(60, 120))

    # Not sure what this is
    xframe = Z_mass.frame(ROOT.RooFit.Title("Test Gaus fit"))
    roo_hist.plotOn(xframe)
    model.plotOn(xframe)
    argset_cmsshape = ROOT.RooArgSet(cmsshape_pdf)
    argset_gauss1 = ROOT.RooArgSet(gauss1_pdf)
    #model.plotOn(xframe, ROOT.RooFit.Components(argset_cmsshape), ROOT.RooFit.LineStyle(ROOT.kDashDotted))
    #model.plotOn(xframe, ROOT.RooFit.Components(argset_gauss1), ROOT.RooFit.LineStyle(ROOT.kDashed))
    model.plotOn(xframe, ROOT.RooFit.Components(argset_cmsshape), ROOT.RooFit.LineStyle(ROOT.kDashDotted), ROOT.RooFit.LineColor(15))
    model.plotOn(xframe, ROOT.RooFit.Components(argset_gauss1), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(15))
    model.Print("t")

    # Make plot
    c = ROOT.TCanvas("output", "output", 600, 600)
    ROOT.gPad.SetLeftMargin(0.15)
    xframe.GetYaxis().SetTitleOffset(1.4)
    xframe.Draw()

    c.SaveAs(in_hist_name+".png")
    print("Chi2=",xframe.chiSquare())

    nsig_final = nsig.getVal()

    print("nsig_final",nsig_final)
    print("nsig_initial",nsig_initial)

    fit_dict = {}
    fit_dict["mean"] = gauss1_mean.getVal()
    fit_dict["sigma"] = gauss1_sigma.getVal()
    fit_dict["nsig"] = nsig.getVal()
    fit_dict["nbkg"] = nbkg.getVal()
    fit_dict["al"] = cmsshape_al.getVal()
    fit_dict["beta"] = cmsshape_beta.getVal()
    fit_dict["lambda"] = cmsshape_lambda0.getVal()
    fit_dict["gamma"] = cmsshape_gamma.getVal()

    #return [nsig_final,nbkg.getVal(),xframe.chiSquare()]
    return fit_dict


def main():

    # Get the input histogram
    #in_file  = ROOT.TFile.Open("flip_hists.root","READ")
    in_file  = ROOT.TFile.Open("flip_hists_mar18_UL17data_allKinCats_eventSelPtCutMaster.root","READ")

    # Get the list of histos to loop over
    histo_name_lst = []
    in_file_keys = in_file.GetListOfKeys()
    for key_object in in_file_keys:
        histo_name_lst.append(key_object.GetName())
    print(histo_name_lst)

    # Fit each histo, save fit params to a dict that we print at the end
    fit_results_dict = {}
    for histo_name in histo_name_lst:
        #if "osz" in histo_name: continue
        if "ssz" in histo_name: continue
        if "EM_EL" in histo_name: continue # This has no Z peak
        if "BH_BH" in histo_name: continue # This has a weird shape in ss
        histo = in_file.Get(histo_name)
        fit_results_dict[histo_name] = do_z_fit(histo,histo_name)

    print "\nFit results:\n",fit_results_dict

if __name__ == "__main__":
    main()

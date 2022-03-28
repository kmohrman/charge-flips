// root -l -b -q write_flip_probs_to_hist.C

// Useful: https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html


void write_flip_probs_to_hist(){

    // Configure the run
    //bool draw_histo = false;
    bool draw_histo = true;
    TString save_name = "mar24_flips_1en3_tmp";

    // Flip probabilities to fill the histo with (hard coded into this script)
    std::vector<double> flip_prob;
    flip_prob = {
        //1.26008646e-03, // EH
        //7.26373920e-04, // EM
        //1.29984835e-04, // EL
        //1.87878947e-04, // BH
        //5.23435609e-05, // BM
        //0.0, // BL
        //1.01161632e-03, // EH
        //5.30454477e-04, // EM
        //4.13351097e-04, // EL
        //4.41565288e-05, // BH
        //7.71973963e-06, // BM
        //5.29044545e-05, // BL
        1.0e-03, // EH (TEST)
        1.0e-03, // EM (TEST)
        1.0e-03, // EL (TEST)
        1.0e-03, // BH (TEST)
        1.0e-03, // BM (TEST)
        1.0e-03, // BL (TEST)
    };

    // Declare the histo
    const Int_t XBINS = 3; const Int_t YBINS = 2;
    Double_t xEdges[XBINS + 1] = {15.0, 25.0, 50.0, 1000000.0};
    //Double_t xEdges[XBINS + 1] = {15.0, 25.0, 50.0, 101.0}; // To see the scale better in the plot
    Double_t yEdges[YBINS + 1] = {0.0, 1.479, 2.5};
    TH2* h2d = new TH2D("flips", "flips", XBINS, xEdges, YBINS, yEdges);

    // Fill the histo (x=pt, y=eta)
    h2d->Fill(100.0, 2.0, flip_prob[0]); // EH
    h2d->Fill(30.0,  2.0, flip_prob[1]); // EM
    h2d->Fill(20.0,  2.0, flip_prob[2]); // EL
    h2d->Fill(100.0, 1.0, flip_prob[3]); // BH
    h2d->Fill(30.0,  1.0, flip_prob[4]); // BM
    h2d->Fill(20.0,  1.0, flip_prob[5]); // BL

    // Make a plot
    if (draw_histo) {
        TCanvas *c1 = new TCanvas("c1","",500,500);
        h2d->Draw("colz");
        c1->Print(save_name+".png","png");
        delete c1;
    }

    // Save the root file
    TFile f(save_name+".root","new");
    h2d->Write();

}

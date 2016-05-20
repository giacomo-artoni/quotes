import ROOT, sys

def main():
  Canvas = ROOT.TCanvas( 'latest_XXX', '', 1000, 600 )
  Chain = ROOT.TChain( '  
  Canvas.SaveAs( '.png' )

if __name__ == '__main__':
  sys.exit( main() )

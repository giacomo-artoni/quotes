import array, datetime, itertools, optparse, re, sys
import ROOT

def main():
  #================#
  parser = optparse.OptionParser()
  parser.add_option( '-i', '--input', dest = 'input_file', action = 'store', type = 'string', default = '', help = '' )
  ( options, args ) = parser.parse_args()
  #================#
  List = [ 'EUR', 'USD', 'CHF', 'GBP' ]
  Dict = {}
  for El1 in List:
    for El2 in List:
      if El1 is not El2:
        Dict[ ( El1, El2 ) ] = None
  #================#
  Date = datetime.date.today()
  Input = '/home/artoni/public_html/quotes/original_pages/page_%s.txt' % Date 
  if options.input_file:
    Input = options.input_file
  for ( El1, El2 ) in Dict:
    the_regex = re.compile( '<td align="left">%s/%s</td><td align="right">([\.\d]+)</td>' % ( El1, El2 ) )
    for line in open( Input, 'r' ).readlines():
      the_match = the_regex.search( line )
      if the_match:
        Dict[ ( El1, El2 ) ] = float( the_match.group( 1 ) )
  #================#
  for ( El1, El2 ) in Dict:
    if not Dict[ ( El1, El2 ) ] and Dict[ ( El2, El1 ) ]:
     Dict[ ( El1, El2 ) ] = 1. / Dict[ ( El2, El1 ) ] 
  for ( El1, El2 ) in Dict:
    if not Dict[ ( El1, El2 ) ]: 
      for El3 in List:
        if El3 is not El1 and El3 is not El2:
          if Dict[ ( El1, El3 ) ] and Dict[ ( El3, El2 ) ]:
            Dict[ ( El1, El2 ) ] = Dict[ ( El1, El3 ) ] * Dict[ ( El3, El2 ) ]
            Dict[ ( El2, El1 ) ] = 1. / ( Dict[ ( El1, El3 ) ] * Dict[ ( El3, El2 ) ] )
  File = ROOT.TFile( Input.replace( 'txt', 'root' ), 'recreate' )
  Tree = ROOT.TTree( 'quotes', '' )
  date_regex = re.compile( 'page_(\d+)-(\d+)-(\d+)' )
  date_match = date_regex.search( Input )
  DateDict = { 1: 'Year', 2: 'Month', 3: 'Day' }
  Index = array.array( 'i', [ datetime.date.toordinal( datetime.date( int( date_match.group( 1 ) ), int( date_match.group( 2 ) ), int( date_match.group( 3 ) ) ) ) ] )
  Tree.Branch( 'Index', Index, 'Index/I' )
  for Key,Val in DateDict.iteritems():
    locals()[ Val ] = array.array( 'i', [ int( date_match.group( Key ) ) ] )
  for Key,Val in DateDict.iteritems():
    Tree.Branch( Val, locals()[ Val ], '%s/I' % Val )
  for El1, El2 in Dict:
    locals()[ 'ar_%s_%s' % ( El1, El2 ) ] = array.array( 'f', [ Dict[ ( El1, El2 ) ] ] )
    Tree.Branch( '%svs%s' % ( El1, El2 ), locals()[ 'ar_%s_%s' % ( El1, El2 ) ], '%svs%s/F' % ( El1, El2 ) ) 
  Tree.Fill()
  File.Write()
  File.Close()

if __name__ == '__main__':
  sys.exit( main() )

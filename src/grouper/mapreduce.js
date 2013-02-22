

/*  def mapfunc(self, maxChar):
    # mongodb wants javascript for map reduce
    # checks: don't join me with myself; 
    #	      if I am a joined ID, ignore me unless I am a max size concatenation;
    #	      if the ID you want to join me with, is already joined, ignore it; */
    function map( maxChar ) {
      self = this;
      if( self.split('_').length < maxChar ) return;
      this._id.forEach( function( x ) {
	if( self._id == x ) return;
	if( x.split('_').length > 1 ) return;
	emit( [self._id, id].sort().join('_'), self.value );
      })
    };

    function reduce( key, values ) {
      return { value : intersect( null, values ) };
      };


    intersect = function( a, b ) {
		a.filter( function(x) { return b.indexOf(x) >= 0; });
	      };

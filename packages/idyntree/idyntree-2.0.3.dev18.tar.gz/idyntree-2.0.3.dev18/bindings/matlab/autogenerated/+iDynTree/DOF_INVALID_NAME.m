function varargout = DOF_INVALID_NAME(varargin)
  narginchk(0,1)
  if nargin==0
    nargoutchk(0,1)
    varargout{1} = iDynTreeMEX(736);
  else
    nargoutchk(0,0)
    iDynTreeMEX(737,varargin{1});
  end
end

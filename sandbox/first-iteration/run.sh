shapes=$1
data=$2

pyshacl -f table -s $shapes -df json-ld -sf turtle $data objreg.jsonld

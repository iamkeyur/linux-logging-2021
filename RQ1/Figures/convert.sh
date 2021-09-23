# http://ctan.mirror.globo.tech/info/svg-inkscape/InkscapePDFLaTeX.pdf
for file in *.svg; do
    inkscape --export-area-drawing --export-filename="$(basename "$file" .svg).pdf" --export-latex "$file" 
done
from oodocument import oodocument
data = []
data.append((23, 28, 'XXX'))
data.append((38, 44, 'XXX'))
oo = oodocument('./input.docx', host='0.0.0.0', port=8001)
oo.replace_with_index(data, './output.pdf', 'pdf')
oo.dispose()

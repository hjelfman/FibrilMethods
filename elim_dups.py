import pandas as pd

def compare_rect(r1,r2):
	#print(str(r1) + " | " + str(r2))
	rect_1 = r1
	rect_2 = r2
	l1 = (r1[0][0],r1[1][1])
	r1 = (rect_1[1][0],rect_1[0][1])
	l2 = (r2[0][0],r2[1][1])
	r2 = (rect_2[1][0],rect_2[0][1])
	if (rect_1 == rect_2):
		#print('same!')
		return False # Do not overlap
	if (l1[0] == r1[0] or l1[1] == r2[1] or l2[0] == r2[0] or l2[1] == r2[1]):
		#print('1')
		return False
	if (l1[0] >= r2[0] or l2[0] >= r1[0]):
		#print('2')
		return False
	if (l1[1] <= r2[1] or l2[1] <= r1[1]):
		#print('3')
		return False
	#print('Intersection!')
	return True

results = pd.read_csv('Detection_Results.csv', index_col=0)
results['tsize'] = ((results['xmax']-results['xmin'])**2 + (results['ymax']-results['ymin'])**2)**0.5
imgs = results.index
lab = results.columns
imgs = list(set(imgs))
finals = []
for img in imgs:
	new = results.xs(img)
	new = pd.DataFrame(new, columns=lab)
	#print(new)
	for index, row in new.iterrows():
			#print(row['xmin'])
			current_rect = [(int(row['xmin']), int(row['ymin'])),(int(row['xmax']), int(row['ymax']))]
			for index2, row2 in new.iterrows():
				new_rect = [(int(row2['xmin']), int(row2['ymin'])),(int(row2['xmax']), int(row2['ymax']))]
				if compare_rect(current_rect, new_rect):
					finals.append(row2)
					#print(row2)

duplicates = pd.DataFrame(finals)
#print(duplicates)
new_w_dup = [results, duplicates]
list_duplicated = pd.concat(new_w_dup)
list_duplicated.drop_duplicates(keep=False, inplace=True) #never overlap

largest = duplicates.groupby(level=0).apply(lambda group: group.nlargest(1, columns='tsize')).reset_index(level=-1, drop=True)

new55 = [list_duplicated, largest]
list_duplicated = pd.concat(new55)
list_duplicated.drop_duplicates(keep=False, inplace=True)
list_duplicated.sort_index(axis=0, inplace=True)

list_duplicated.to_csv('new_results.csv')
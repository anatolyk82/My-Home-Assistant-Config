#!/bin/bash

DIR=/home/homeassistant/.homeassistant/www/camera_records

files=`ls $DIR/*.mp4`
html_file="$DIR/index.html"

echo > $html_file

cat <<EOF >$html_file
<html>
	<head>
		<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/siimple@3.3.1/dist/siimple.min.css">
	</head>
	<body>
		<div class="siimple-content siimple-content--large siimple--mt-5">
			<div class="siimple-grid">
				<div class="siimple-grid-row">
EOF

row=0
for f in $files
do
	name=`basename $f`
	camera_name=`echo $name | cut -d'_' -f1`
	record_date_raw=`echo $name | cut -d'_' -f2 | cut -d'.' -f1`
	str_date=`echo $record_date_raw | cut -d'-' -f1`
	str_time=`echo $record_date_raw | cut -d'-' -f2`
	r_date=`date -d $str_date +'%Y-%m-%d'`
cat <<EOF >> $html_file
					<div class="siimple-grid-col siimple-grid-col--4 siimple-grid-col--sm-12">
						<div class="siimple-card">
							<div class="siimple-card-header" align="center">$camera_name</div>
							<div class="siimple-card-body" align="center">
								<video width="280" height="160" controls><source src="$name" type="video/mp4"/></video>
							</div>
							<div class="siimple-card-footer" align="center">$r_date $str_time</div>
						</div>
					</div>
EOF
if [ $row == 2 ]
then
cat << EOF >> $html_file
				</div>
				<div class="siimple-grid-row">
EOF
row=0
else
row=`expr $row + 1`
fi


done

cat <<EOF >> $html_file
				</div>
			</div>
		</div>
	</body>
</html>
EOF

#echo "<br/><a href='/lovelace/overview'>Back to Home Assistant</a><br/>" >> $html_file

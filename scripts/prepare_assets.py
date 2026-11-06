"""One-time image preparation. Requires Pillow; production builds do not."""
from PIL import Image, ImageOps
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'upload'
items=[
 ('_DSC3057.jpg','mountain-engagement','Couple holding white roses in a green mountain meadow','couples'),
 ('DSC_0990.jpg','engagement-ring','Engagement ring with flowers and a soft blue sleeve','couples'),
 ('_DSC0373.jpg','family-hillside','Family of five together on a green hillside','families'),
 ('_DSC0392.jpg','missionary-portrait','Missionary in a navy suit holding a Spanish Book of Mormon beside a fence','portraits'),
 ('_DSC2979.jpg','meadow-proposal','Surprise proposal on a blanket surrounded by candles and flowers','couples'),
 ('_DSC4206 copy.jpg','family-under-tree','Parents and two young children sitting together beneath a tree','families'),
 ('_DSC1296.jpg','garden-portrait','Portrait among yellow roses and green leaves','portraits'),
 ('_DSC2739.jpg','sunset-couple','Couple silhouetted against an orange sunset over the water','couples'),
 ('_DSC3249.jpg','culinary-event','Chef adding the finishing touches to dinner plates at a culinary event','events'),
 ('_DSC6877.jpg','autumn-proposal','A marriage proposal beneath a flower-covered arch in autumn','couples'),
 ('DSC_8726.jpg','graduation-celebration','Graduate laughing and raising her cap on a woodland path','seniors'),
 ('_DSC1149.jpg','window-light-portrait','Warm window light falling across a portrait in a satin dress','portraits'),
 ('_DSC5797.jpg','lakeside-couple','Couple kissing by a mountain lake at sunset with a paraglider above','couples'),
 ('DSC_8931.jpg','stone-doorway-portrait','Senior portrait in a white shirt and blue jeans by a stone doorway','seniors'),
 ('DSC_8747.jpg','graduation-river','Graduate in cap and gown standing beside a river','seniors'),
 ('_DSC6951.jpg','quiet-embrace','Newly engaged couple sharing a close embrace','couples'),
 ('_DSC5623.jpg','lakeside-family','Family of five smiling beside a lake and mountains','families')]
items += [("Trevor.Adair'sPhotos-20.jpg", 'temple-garden-portrait', 'Portrait in a white dress beside colorful flowers and brick architecture', 'portraits'), ('DSC_8758.jpg', 'orchard-senior', 'Senior portrait along a green orchard path', 'seniors'), ('_DSC2482.jpg', 'dinner-event-setting', 'Long tables set with flowers and glassware for an evening event', 'events'), ('_DSC5978.jpg', 'guitar-portrait', 'Outdoor portrait with an acoustic guitar in warm evening light', 'portraits'), ('_DSC5931.jpg', 'dandelion-portrait', 'A woman blowing dandelion seeds in a sunlit garden', 'portraits'), ("Trevor.Adair'sPhotos-54.jpg", 'missionary-temple-gates', 'Missionary in a red dress holding a Chinese Book of Mormon at temple gates', 'portraits'), ('_DSC6998.jpg', 'engaged-hands', 'Couple holding hands with an engagement ring in autumn light', 'couples'), ('_DSC2571.jpg', 'proposal-surprise', 'Smiling man guiding his blindfolded partner toward a surprise', 'couples'), ("Trevor.Adair'sPhotos-25.jpg", 'missionary-reading', 'Missionary seated reading a Book of Mormon outside a brick temple', 'portraits'), ('_DSC6995.jpg', 'archway-portrait', 'Portrait in a floral dress framed by an ornate stone arch', 'portraits'), ('_DSC2589.jpg', 'proposal-arrival', 'Couple approaching a candlelit proposal setup at dusk', 'couples'), ("Trevor.Adair'sPhotos-7.jpg", 'missionary-temple-portrait', 'Missionary in a white dress standing in front of a temple garden', 'portraits'), ("Trevor.Adair'sPhotos-2.jpg", 'missionary-steps', 'Missionary portrait on stone steps beside a black railing', 'portraits'), ('image (7).jpg', 'family-garden-bridge', 'Family of six together on a garden bridge', 'families'), ('_DSC2472.jpg', 'culinary-spread', 'Cured ham, pastries and fruit arranged for a culinary gathering', 'events'), ('_DSC4409.jpg', 'prom-flowers', 'White corsage and boutonniere against a navy suit', 'events'), ('_DSC5828.jpg', 'sunlit-grass-portrait', 'Relaxed portrait seated in grass beneath warm sunbeams', 'portraits'), ('_DSC4461.jpg', 'couple-under-tree', 'Smiling couple sitting together against a broad tree trunk', 'couples'), ('_DSC9404.jpg', 'missionary-stone-arch', 'Missionary in a navy suit holding a Portuguese Book of Mormon beneath a stone arch', 'portraits'), ('_DSC8996 (1).jpg', 'trevor-adair-bio', 'Trevor Adair holding his Nikon camera on a green orchard path', 'bio')]
assets=root/'dist/assets';assets.mkdir(parents=True,exist_ok=True)
meta=[]
for original,slug,alt,category in items:
 im=ImageOps.exif_transpose(Image.open(source/original)).convert('RGB')
 widths=[]
 for w in [480,960,1600,2048]:
  if w>im.width and widths:continue
  w=min(w,im.width); resized=im.resize((w,round(w*im.height/im.width)),Image.Resampling.LANCZOS)
  resized.save(assets/f'{slug}-{w}.webp','WEBP',quality=84,method=6)
  widths.append(w)
 meta.append(dict(slug=slug,alt=alt,category=category,width=im.width,height=im.height,widths=widths,original=original))
(root/'src/images.json').write_text(json.dumps(meta,indent=2))
print(f'Prepared {len(meta)} photographs without EXIF or GPS metadata.')

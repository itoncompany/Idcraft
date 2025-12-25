import pandas as pd
from io import StringIO

# The original CSV data with the addresses now enclosed in double quotes (")
csv_data_fixed = """
full_name,roll,dob,gender,email,student_phone,parent_name,parent_phone,address,school,grade,section,valid_until,status
Leo Messi,301,2010-06-24,MALE,leo.m@example.com,980000101,Celia Messi,980000201,"10 Park Ave, East City",Bright Academy,5,A,2026-06-24,ACTIVE
Serena Williams,302,2011-09-26,FEMALE,serena.w@example.com,980000102,Richard Williams,980000202,"20 Oak St, West Town",Bright Academy,4,B,2026-09-26,NEW
Roger Federer,303,2009-08-08,MALE,roger.f@example.com,980000103,Lynette Federer,980000203,"30 Elm Rd, North City",Sunset School,6,C,2025-08-08,ACTIVE
Naomi Osaka,304,2012-10-16,FEMALE,naomi.o@example.com,980000104,Leonard Osaka,980000204,"40 Pine Ln, South Village",Bright Academy,3,A,2027-10-16,ACTIVE
Rafael Nadal,305,2008-06-03,MALE,rafael.n@example.com,980000105,Sebastian Nadal,980000205,"50 Maple Dr, Central City",Sunset School,7,B,2025-06-03,INACTIVE
Maria Sharapova,306,2013-04-19,FEMALE,maria.s@example.com,980000106,Yuri Sharapova,980000206,"60 Birch Ct, East City",Bright Academy,2,C,2027-04-19,ACTIVE
Novak Djokovic,307,2010-05-22,MALE,novak.d@example.com,980000107,Dijana Djokovic,980000207,"70 Cedar Blvd, West Town",Sunset School,5,A,2026-05-22,NEW
Venus Williams,308,2011-06-17,FEMALE,venus.w@example.com,980000108,Oracene Williams,980000208,"80 Willow St, North City",Bright Academy,4,B,2026-06-17,ACTIVE
Andy Murray,309,2009-05-15,MALE,andy.m@example.com,980000109,Judy Murray,980000209,"90 Ash Ln, South Village",Sunset School,6,C,2025-05-15,ACTIVE
Simona Halep,310,2012-09-27,FEMALE,simona.h@example.com,980000110,Stere Halep,980000210,"100 Poplar Dr, Central City",Bright Academy,3,A,2027-09-27,INACTIVE
Dominic Thiem,311,2008-09-03,MALE,dominic.t@example.com,980000111,Wolfgang Thiem,980000211,"110 Spruce Ave, East City",Sunset School,7,B,2025-09-03,ACTIVE
Bianca Andreescu,312,2013-06-16,FEMALE,bianca.a@example.com,980000112,Nicu Andreescu,980000212,"120 Redwood Rd, West Town",Bright Academy,2,C,2027-06-16,NEW
Daniil Medvedev,313,2010-02-11,MALE,daniil.m@example.com,980000113,Sergey Medvedev,980000213,"130 Sycamore Ln, North City",Sunset School,5,A,2026-02-11,ACTIVE
Elina Svitolina,314,2011-09-12,FEMALE,elina.s@example.com,980000114,Mikhail Svitolina,980000214,"140 Walnut St, South Village",Bright Academy,4,B,2026-09-12,ACTIVE
Alexander Zverev,315,2009-04-20,MALE,alexander.z@example.com,980000115,Alexander Zverev Sr,980000215,"150 Chestnut Dr, Central City",Sunset School,6,C,2025-04-20,ACTIVE
Ashleigh Barty,316,2012-04-24,FEMALE,ashleigh.b@example.com,980000116,Josie Barty,980000216,"160 Hemlock Ct, East City",Bright Academy,3,A,2027-04-24,INACTIVE
Stefanos Tsitsipas,317,2008-08-12,MALE,stefanos.t@example.com,980000117,Apostolos Tsitsipas,980000217,"170 Elder Ave, West Town",Sunset School,7,B,2025-08-12,NEW
Garbine Muguruza,318,2013-10-08,FEMALE,garbine.m@example.com,980000118,Jose Muguruza,980000218,"180 Fir Ln, North City",Bright Academy,2,C,2027-10-08,ACTIVE
Andrey Rublev,319,2010-10-20,MALE,andrey.r@example.com,980000119,Marina Marenko,980000219,"190 Redwood St, South Village",Sunset School,5,A,2026-10-20,ACTIVE
Karolina Pliskova,320,2011-03-21,FEMALE,karolina.p@example.com,980000120,Radek Plisek,980000220,"200 Spruce Dr, Central City",Bright Academy,4,B,2026-03-21,ACTIVE
Matteo Berrettini,321,2009-04-14,MALE,matteo.b@example.com,980000121,Luca Berrettini,980000221,"210 Pine Ave, East City",Sunset School,6,C,2025-04-14,NEW
Coco Gauff,322,2012-03-13,FEMALE,coco.g@example.com,980000122,Cori Gauff,980000222,"220 Maple Ln, West Town",Bright Academy,3,A,2027-03-13,ACTIVE
Denis Shapovalov,323,2008-04-15,MALE,denis.s@example.com,980000123,Tessa Shapovalova,980000223,"230 Oak St, North City",Sunset School,7,B,2025-04-15,ACTIVE
Iga Swiatek,324,2013-05-31,FEMALE,iga.s@example.com,980000124,Tomasz Swiatek,980000224,"240 Elm Rd, South Village",Bright Academy,2,C,2027-05-31,INACTIVE
Jannik Sinner,325,2010-08-16,MALE,jannik.s@example.com,980000125,Hanspeter Sinner,980000225,"250 Cedar Dr, Central City",Sunset School,5,A,2026-08-16,ACTIVE
Petra Kvitova,326,2011-03-08,FEMALE,petra.k@example.com,980000126,Jiri Kvita,980000226,"260 Willow Ct, East City",Bright Academy,4,B,2026-03-08,NEW
Grigor Dimitrov,327,2009-05-16,MALE,grigor.d@example.com,980000127,Dimitre Dimitrov,980000227,"270 Ash Blvd, West Town",Sunset School,6,C,2025-05-16,ACTIVE
Madison Keys,328,2012-02-17,FEMALE,madison.k@example.com,980000128,Rick Keys,980000228,"280 Poplar St, North City",Bright Academy,3,A,2027-02-17,ACTIVE
Stan Wawrinka,329,2008-03-28,MALE,stan.w@example.com,980000129,Nicole Wawrinka,980000229,"290 Redwood Ave, South Village",Sunset School,7,B,2025-03-28,ACTIVE
Victoria Azarenka,330,2013-07-31,FEMALE,victoria.a@example.com,980000130,Alla Azarenka,980000230,"300 Sycamore Dr, Central City",Bright Academy,2,C,2027-07-31,INACTIVE
Kei Nishikori,331,2010-12-29,MALE,kei.n@example.com,980000131,Kiyoshi Nishikori,980000231,"310 Walnut Ct, East City",Sunset School,5,A,2026-12-29,ACTIVE
Angelique Kerber,332,2011-01-18,FEMALE,angelique.k@example.com,980000132,Slawomir Kerber,980000232,"320 Chestnut Rd, West Town",Bright Academy,4,B,2026-01-18,NEW
Milos Raonic,333,2009-12-27,MALE,milos.r@example.com,980000133,Dusan Raonic,980000233,"330 Hemlock Blvd, North City",Sunset School,6,C,2025-12-27,ACTIVE
Sloane Stephens,334,2012-03-20,FEMALE,sloane.s@example.com,980000134,Sybil Stephens,980000234,"340 Elder St, South Village",Bright Academy,3,A,2027-03-20,ACTIVE
Marin Cilic,335,2008-09-28,MALE,marin.c@example.com,980000135,Zdenko Cilic,980000235,"350 Fir Ln, Central City",Sunset School,7,B,2025-09-28,ACTIVE
Aryna Sabalenka,336,2013-05-05,FEMALE,aryna.s@example.com,980000136,Sergey Sabalenka,980000236,"360 Redwood Ave, East City",Bright Academy,2,C,2027-05-05,INACTIVE
Gael Monfils,337,2010-09-01,MALE,gael.m@example.com,980000137,Sylvette Monfils,980000237,"370 Spruce Dr, West Town",Sunset School,5,A,2026-09-01,NEW
Johanna Konta,338,2011-07-17,FEMALE,johanna.k@example.com,980000138,Gabor Konta,980000238,"380 Pine St, North City",Bright Academy,4,B,2026-07-17,ACTIVE
Richard Gasquet,339,2009-06-18,MALE,richard.g@example.com,980000139,Francis Gasquet,980000239,"390 Maple Ct, South Village",Sunset School,6,C,2025-06-18,ACTIVE
Donna Vekic,340,2012-06-28,FEMALE,donna.v@example.com,980000140,Branko Vekic,980000240,"400 Oak Blvd, Central City",Bright Academy,3,A,2027-06-28,ACTIVE
Fabio Fognini,341,2008-05-24,MALE,fabio.f@example.com,980000141,Silvana Fognini,980000241,"410 Cedar Ln, East City",Sunset School,7,B,2025-05-24,ACTIVE
Karolina Muchova,342,2013-08-21,FEMALE,karolina.m@example.com,980000142,Jiri Mucha,980000242,"420 Elm Ave, West Town",Bright Academy,2,C,2027-08-21,INACTIVE
Roberto Bautista,343,2010-04-14,MALE,roberto.b@example.com,980000143,Javier Bautista,980000243,"430 Birch Dr, North City",Sunset School,5,A,2026-04-14,NEW
Dan Evans,344,2011-05-23,FEMALE,dan.e@example.com,980000144,Bernice Evans,980000244,"440 Willow St, South Village",Bright Academy,4,B,2026-05-23,ACTIVE
Felix Auger,345,2009-08-08,MALE,felix.a@example.com,980000145,Sam Aliassime,980000245,"450 Ash Ct, Central City",Sunset School,6,C,2025-08-08,ACTIVE
Anett Kontaveit,346,2012-01-24,FEMALE,anett.k@example.com,980000146,Urmas Kontaveit,980000246,"460 Poplar Blvd, East City",Bright Academy,3,A,2027-01-24,ACTIVE
Benoit Paire,347,2008-05-08,MALE,benoit.p@example.com,980000147,Philippe Paire,980000247,"470 Redwood Ln, West Town",Sunset School,7,B,2025-05-08,ACTIVE
Svetlana Kuznetsova,348,2013-06-27,FEMALE,svetlana.k@example.com,980000148,Galina Kuznetsova,980000248,"480 Sycamore Ave, North City",Bright Academy,2,C,2027-06-27,NEW
Karen Khachanov,349,2010-05-21,MALE,karen.k@example.com,980000149,Arakel Khachanov,980000249,"490 Walnut Dr, South Village",Sunset School,5,A,2026-05-21,ACTIVE
Elise Mertens,350,2011-11-17,FEMALE,elise.m@example.com,980000150,Karin Mertens,980000250,"500 Chestnut Ct, Central City",Bright Academy,4,B,2026-11-17,ACTIVE
"""

# Read the fixed CSV data into a pandas DataFrame
df = pd.read_csv(StringIO(csv_data_fixed))

# Convert appropriate columns to desired types (This should now work)
df['roll'] = df['roll'].astype(int)
df['grade'] = df['grade'].astype(int)
df['dob'] = pd.to_datetime(df['dob'])
df['valid_until'] = pd.to_datetime(df['valid_until'])

# Define the Excel file name
excel_file_name = 'student_records_fixed.xlsx'

# Save the DataFrame to the Excel file
try:
    df.to_excel(excel_file_name, sheet_name='Student Data', index=False)
    print(f"Successfully created and saved the Excel file: '{excel_file_name}'")
except Exception as e:
    print(f"An error occurred while saving the Excel file: {e}")
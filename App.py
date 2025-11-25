from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import random
import os
import sys

app = Flask(__name__)

REAL_ARTIFACTS = [
    {
        'id': 1,
        'name': 'Rosetta Stone',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1801,
        'description': 'The key that unlocked Egyptian hieroglyphs. Contains the same text in three scripts: hieroglyphic, demotic, and Greek. Captured from French forces by the British.',
        'artifact_type': 'Granodiorite Stone',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/rosetta_stone.jpg',
        'images': ['/static/images/rosetta_1.jpg', '/static/images/rosetta_2.jpg']
    },
    {
        'id': 2,
        'name': 'Bust of Nefertiti',
        'museum': 'Neues Museum',
        'city': 'Berlin',
        'country': 'Germany',
        'latitude': 52.5200,
        'longitude': 13.3967,
        'status': 'Contested',
        'year_taken': 1912,
        'description': 'Iconic limestone bust of Queen Nefertiti, renowned for its beauty and preservation. Acquired by German archaeologist Ludwig Borchardt under disputed circumstances.',
        'artifact_type': 'Limestone Bust',
        'current_location': 'Neues Museum, Berlin',
        'image_url': '/static/images/nefertiti_bust.jpg',
        'images': ['/static/images/nefertiti_1.jpg', '/static/images/nefertiti_2.jpg']
    },
    {
        'id': 3,
        'name': 'Dendera Zodiac',
        'museum': 'Louvre Museum',
        'city': 'Paris',
        'country': 'France',
        'latitude': 48.8606,
        'longitude': 2.3376,
        'status': 'Contested',
        'year_taken': 1820,
        'description': 'Celestial bas-relief from the Temple of Hathor ceiling. Removed by French archaeologist Sébastien Louis Saulnier using saws and explosives.',
        'artifact_type': 'Sandstone Relief',
        'current_location': 'Louvre Museum, Paris',
        'image_url': '/static/images/dendera_zodiac.jpg',
        'images': ['/static/images/dendera_1.jpg', '/static/images/dendera_2.jpg']
    },
    {
        'id': 4,
        'name': 'Colossal Statue of Ramesses II',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1818,
        'description': '7.5-ton granite statue of Pharaoh Ramesses II from the Ramesseum temple. Transported to England by Giovanni Belzoni.',
        'artifact_type': 'Granite Statue',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/ramesses_british.jpg',
        'images': ['/static/images/ramesses_1.jpg']
    },
    {
        'id': 5,
        'name': 'Temple of Dendur',
        'museum': 'Metropolitan Museum of Art',
        'city': 'New York',
        'country': 'USA',
        'latitude': 40.7794,
        'longitude': -73.9631,
        'status': 'Contested',
        'year_taken': 1965,
        'description': 'Complete Roman-era temple gifted to the US after Aswan Dam construction. Originally built around 15 BCE by Roman governor Petronius.',
        'artifact_type': 'Sandstone Temple',
        'current_location': 'Metropolitan Museum of Art, New York',
        'image_url': '/static/images/dendur_temple.jpg',
        'images': ['/static/images/dendur_1.jpg', '/static/images/dendur_2.jpg']
    },
    {
        'id': 6,
        'name': 'Sarcophagus of Seti I',
        'museum': 'Sir John Soane\'s Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5175,
        'longitude': -0.1167,
        'status': 'Contested',
        'year_taken': 1821,
        'description': 'Magnificent alabaster sarcophagus of Pharaoh Seti I, father of Ramesses II. Acquired by Giovanni Belzoni from the Valley of the Kings.',
        'artifact_type': 'Alabaster Sarcophagus',
        'current_location': 'Sir John Soane\'s Museum, London',
        'image_url': '/static/images/seti_sarcophagus.jpg',
        'images': ['/static/images/seti_1.jpg']
    },
    {
        'id': 7,
        'name': 'Statue of Hemiunu',
        'museum': 'Roemer und Pelizaeus Museum',
        'city': 'Hildesheim',
        'country': 'Germany',
        'latitude': 52.1500,
        'longitude': 9.9500,
        'status': 'Contested',
        'year_taken': 1912,
        'description': 'Life-sized limestone statue of Hemiunu, nephew of Pharaoh Khufu and probable architect of the Great Pyramid. Found in his mastaba tomb at Giza.',
        'artifact_type': 'Limestone Statue',
        'current_location': 'Roemer und Pelizaeus Museum, Hildesheim',
        'image_url': '/static/images/hemiunu.jpg',
        'images': ['/static/images/hemiunu_1.jpg']
    },
    {
        'id': 8,
        'name': 'Green Head of Osiris',
        'museum': 'Egyptian Museum of Berlin',
        'city': 'Berlin',
        'country': 'Germany',
        'latitude': 52.5200,
        'longitude': 13.3967,
        'status': 'Contested',
        'year_taken': 1911,
        'description': 'Exquisite basalt head of Osiris from the Late Period. Considered one of the finest examples of Egyptian sculpture in existence.',
        'artifact_type': 'Basalt Sculpture',
        'current_location': 'Egyptian Museum of Berlin',
        'image_url': '/static/images/green_head.jpg',
        'images': ['/static/images/green_head_1.jpg']
    },
    {
        'id': 9,
        'name': 'Statue of Ka-Aper',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1860,
        'description': 'Wooden statue of a priest from the 5th Dynasty. Known as "Sheikh el-Balad" (Village Chief) due to its lifelike appearance. Found at Saqqara.',
        'artifact_type': 'Wooden Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/ka_aper.jpg',
        'images': ['/static/images/ka_aper_1.jpg']
    },
    {
        'id': 10,
        'name': 'Sphinx of Hatshepsut',
        'museum': 'Metropolitan Museum of Art',
        'city': 'New York',
        'country': 'USA',
        'latitude': 40.7794,
        'longitude': -73.9631,
        'status': 'Contested',
        'year_taken': 1930,
        'description': 'Granite sphinx bearing the features of Pharaoh Hatshepsut. One of several sphinxes from her temple at Deir el-Bahri.',
        'artifact_type': 'Granite Sphinx',
        'current_location': 'Metropolitan Museum of Art, New York',
        'image_url': '/static/images/hatshepsut_sphinx.jpg',
        'images': ['/static/images/hatshepsut_1.jpg']
    },
    {
        'id': 11,
        'name': 'Narmer Palette',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1898,
        'description': 'Ceremonial palette commemorating the unification of Upper and Lower Egypt under King Narmer. One of the earliest historical documents from ancient Egypt.',
        'artifact_type': 'Slate Palette',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/narmer_palette.jpg',
        'images': ['/static/images/narmer_1.jpg']
    },
    {
        'id': 12,
        'name': 'Bust of Ankhhaf',
        'museum': 'Museum of Fine Arts',
        'city': 'Boston',
        'country': 'USA',
        'latitude': 42.3393,
        'longitude': -71.0940,
        'status': 'Contested',
        'year_taken': 1925,
        'description': 'Limestone bust of Prince Ankhhaf, son of Pharaoh Sneferu. Considered one of the masterpieces of Old Kingdom portraiture.',
        'artifact_type': 'Limestone Bust',
        'current_location': 'Museum of Fine Arts, Boston',
        'image_url': '/static/images/ankhhaf.jpg',
        'images': ['/static/images/ankhhaf_1.jpg']
    },
    {
        'id': 13,
        'name': 'Statue of Khafre',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1860,
        'description': 'Diorite statue of Pharaoh Khafre, builder of the second pyramid at Giza. Found in his valley temple by Auguste Mariette.',
        'artifact_type': 'Diorite Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/khafre.jpg',
        'images': ['/static/images/khafre_1.jpg']
    },
    {
        'id': 14,
        'name': 'Seated Statue of Hatshepsut',
        'museum': 'Metropolitan Museum of Art',
        'city': 'New York',
        'country': 'USA',
        'latitude': 40.7794,
        'longitude': -73.9631,
        'status': 'Contested',
        'year_taken': 1930,
        'description': 'Large seated statue of Pharaoh Hatshepsut in traditional royal regalia. From her mortuary temple at Deir el-Bahri.',
        'artifact_type': 'Granite Statue',
        'current_location': 'Metropolitan Museum of Art, New York',
        'image_url': '/static/images/hatshepsut_seated.jpg',
        'images': ['/static/images/hatshepsut_2.jpg']
    },
    {
        'id': 15,
        'name': 'Mummy Mask of Satdjehuty',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1827,
        'description': 'Gilded cartonnage mummy mask of Queen Satdjehuty, daughter of Pharaoh Seqenenre Tao. From her tomb at Thebes.',
        'artifact_type': 'Gilded Mask',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/satdjehuty_mask.jpg',
        'images': ['/static/images/satdjehuty_1.jpg']
    },
    {
        'id': 16,
        'name': 'Statue of Amenhotep III and Tiye',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1889,
        'description': 'Colossal statue depicting Pharaoh Amenhotep III with his wife Queen Tiye. From the temple at Medinet Habu.',
        'artifact_type': 'Quartzite Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/amenhotep_tiye.jpg',
        'images': ['/static/images/amenhotep_1.jpg']
    },
    {
        'id': 17,
        'name': 'Bust of Akhenaten',
        'museum': 'Louvre Museum',
        'city': 'Paris',
        'country': 'France',
        'latitude': 48.8606,
        'longitude': 2.3376,
        'status': 'Contested',
        'year_taken': 1922,
        'description': 'Sandstone bust of the "heretic pharaoh" Akhenaten, showing the distinctive Amarna artistic style. From Karnak temple.',
        'artifact_type': 'Sandstone Bust',
        'current_location': 'Louvre Museum, Paris',
        'image_url': '/static/images/akhenaten_bust.jpg',
        'images': ['/static/images/akhenaten_1.jpg']
    },
    {
        'id': 18,
        'name': 'Golden Throne of Tutankhamun',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1922,
        'description': 'Exquisitely crafted golden throne found in Tutankhamun\'s tomb. Features the young king with his wife Ankhesenamun.',
        'artifact_type': 'Golden Throne',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/tut_throne.jpg',
        'images': ['/static/images/tut_throne_1.jpg']
    },
    {
        'id': 19,
        'name': 'Rosicrucian Egyptian Museum Collection',
        'museum': 'Rosicrucian Egyptian Museum',
        'city': 'San Jose',
        'country': 'USA',
        'latitude': 37.3329,
        'longitude': -121.9046,
        'status': 'Contested',
        'year_taken': 1930,
        'description': 'Large collection of Egyptian artifacts including mummies, sarcophagi, and funerary objects acquired through various expeditions.',
        'artifact_type': 'Museum Collection',
        'current_location': 'Rosicrucian Egyptian Museum, San Jose',
        'image_url': '/static/images/rosicrucian.jpg',
        'images': ['/static/images/rosicrucian_1.jpg']
    },
    {
        'id': 20,
        'name': 'Statue of Senusret III',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1838,
        'description': 'Granite statue of the powerful Middle Kingdom pharaoh Senusret III, known for his military campaigns and administrative reforms.',
        'artifact_type': 'Granite Statue',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/senusret_iii.jpg',
        'images': ['/static/images/senusret_1.jpg']
    },
    {
        'id': 21,
        'name': 'Temple of Taffeh',
        'museum': 'Rijksmuseum van Oudheden',
        'city': 'Leiden',
        'country': 'Netherlands',
        'latitude': 52.1583,
        'longitude': 4.4853,
        'status': 'Contested',
        'year_taken': 1970,
        'description': 'Roman-era temple originally from Taffeh, Egypt. Gifted to the Netherlands for help saving Nubian monuments during Aswan Dam construction.',
        'artifact_type': 'Sandstone Temple',
        'current_location': 'Rijksmuseum van Oudheden, Leiden',
        'image_url': '/static/images/taffeh_temple.jpg',
        'images': ['/static/images/taffeh_1.jpg']
    },
    {
        'id': 22,
        'name': 'Sarcophagus of Nedjemankh',
        'museum': 'Returned to Egypt',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'Returned',
        'year_taken': 2011,
        'description': 'Gilded silver coffin of a high priest. Looted after the 2011 revolution and returned by the Metropolitan Museum in 2019 after investigation.',
        'artifact_type': 'Gilded Coffin',
        'current_location': 'Grand Egyptian Museum, Cairo',
        'image_url': '/static/images/nedjemankh.jpg',
        'images': ['/static/images/nedjemankh_1.jpg']
    },
    {
        'id': 23,
        'name': 'Statue of Mentuhotep II',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1898,
        'description': 'Sandstone statue of Pharaoh Mentuhotep II, the ruler who reunified Egypt and began the Middle Kingdom. From his mortuary temple at Deir el-Bahri.',
        'artifact_type': 'Sandstone Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/mentuhotep.jpg',
        'images': ['/static/images/mentuhotep_1.jpg']
    },
    {
        'id': 24,
        'name': 'Bust of Cleopatra VII',
        'museum': 'Altes Museum',
        'city': 'Berlin',
        'country': 'Germany',
        'latitude': 52.5200,
        'longitude': 13.3967,
        'status': 'Contested',
        'year_taken': 1840,
        'description': 'Marble bust believed to depict Cleopatra VII, the last active ruler of the Ptolemaic Kingdom of Egypt.',
        'artifact_type': 'Marble Bust',
        'current_location': 'Altes Museum, Berlin',
        'image_url': '/static/images/cleopatra_bust.jpg',
        'images': ['/static/images/cleopatra_1.jpg']
    },
    {
        'id': 25,
        'name': 'Canopic Jar of Tutankhamun',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1922,
        'description': 'One of four alabaster canopic jars that contained the internal organs of King Tutankhamun. Each jar protected by a goddess.',
        'artifact_type': 'Alabaster Jar',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/tut_canopic.jpg',
        'images': ['/static/images/tut_canopic_1.jpg']
    },
    {
        'id': 26,
        'name': 'Statue of Ptah',
        'museum': 'Louvre Museum',
        'city': 'Paris',
        'country': 'France',
        'latitude': 48.8606,
        'longitude': 2.3376,
        'status': 'Contested',
        'year_taken': 1826,
        'description': 'Bronze statue of the creator god Ptah, patron deity of craftsmen and architects. From the temple at Memphis.',
        'artifact_type': 'Bronze Statue',
        'current_location': 'Louvre Museum, Paris',
        'image_url': '/static/images/ptah_statue.jpg',
        'images': ['/static/images/ptah_1.jpg']
    },
    {
        'id': 27,
        'name': 'Mummy Mask of Wendjebauendjed',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1940,
        'description': 'Silver and gold mummy mask of General Wendjebauendjed from the 21st Dynasty. One of the few silver masks from ancient Egypt.',
        'artifact_type': 'Silver Mask',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/wendjebauendjed.jpg',
        'images': ['/static/images/wendjebauendjed_1.jpg']
    },
    {
        'id': 28,
        'name': 'Statue of Sekhmet',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1818,
        'description': 'Granite statue of the lion-headed goddess Sekhmet from the temple of Mut at Karnak. One of hundreds commissioned by Amenhotep III.',
        'artifact_type': 'Granite Statue',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/sekhmet.jpg',
        'images': ['/static/images/sekhmet_1.jpg']
    },
    {
        'id': 29,
        'name': 'Fayum Mummy Portraits',
        'museum': 'Various Museums Worldwide',
        'city': 'Multiple Cities',
        'country': 'Multiple Countries',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1880,
        'description': 'Collection of realistic portraits attached to mummies from Roman Egypt. Scattered across museums in Europe and America.',
        'artifact_type': 'Mummy Portraits',
        'current_location': 'Various International Museums',
        'image_url': '/static/images/fayum_portraits.jpg',
        'images': ['/static/images/fayum_1.jpg']
    },
    {
        'id': 30,
        'name': 'Statue of Ankhwa',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1890,
        'description': 'One of the earliest metal statues from ancient Egypt, depicting the shipbuilder Ankhwa from the 3rd Dynasty.',
        'artifact_type': 'Bronze Statue',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/ankhwa.jpg',
        'images': ['/static/images/ankhwa_1.jpg']
    },
    {
        'id': 31,
        'name': 'Kalabsha Gate',
        'museum': 'Egyptian Museum of Berlin',
        'city': 'Berlin',
        'country': 'Germany',
        'latitude': 52.5200,
        'longitude': 13.3967,
        'status': 'Contested',
        'year_taken': 1812,
        'description': 'Large Roman-era gate from Kalabsha Temple in Nubia. Saved from flooding and relocated to Germany.',
        'artifact_type': 'Stone Gate',
        'current_location': 'Egyptian Museum, Berlin',
        'image_url': '/static/images/kalabsha_gate.jpg',
        'images': ['/static/images/kalabsha_1.jpg']
    },
    {
        'id': 32,
        'name': 'Statue of Merneptah',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1896,
        'description': 'Granite statue of Pharaoh Merneptah, son of Ramesses II. Known for his victory stele that contains the first known reference to Israel.',
        'artifact_type': 'Granite Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/merneptah.jpg',
        'images': ['/static/images/merneptah_1.jpg']
    },
    {
        'id': 33,
        'name': 'Coffin of Hor',
        'museum': 'Louvre Museum',
        'city': 'Paris',
        'country': 'France',
        'latitude': 48.8606,
        'longitude': 2.3376,
        'status': 'Contested',
        'year_taken': 1824,
        'description': 'Painted wooden coffin of the priest Hor from the Late Period. Notable for its vivid colors and detailed hieroglyphs.',
        'artifact_type': 'Wooden Coffin',
        'current_location': 'Louvre Museum, Paris',
        'image_url': '/static/images/hor_coffin.jpg',
        'images': ['/static/images/hor_1.jpg']
    },
    {
        'id': 34,
        'name': 'Statue of Niankhkhnum and Khnumhotep',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1964,
        'description': 'Unique double statue of two royal manicurists shown embracing. Their close relationship has been subject of much scholarly discussion.',
        'artifact_type': 'Limestone Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/niankhkhnum.jpg',
        'images': ['/static/images/niankhkhnum_1.jpg']
    },
    {
        'id': 35,
        'name': 'Sphinx of Taharqa',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1932,
        'description': 'Granite sphinx with the features of Pharaoh Taharqa, the Nubian ruler of the 25th Dynasty who controlled both Egypt and Kush.',
        'artifact_type': 'Granite Sphinx',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/taharqa_sphinx.jpg',
        'images': ['/static/images/taharqa_1.jpg']
    },
    {
        'id': 36,
        'name': 'Statue of Khentkawes I',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1932,
        'description': 'Diorite statue of Queen Khentkawes I, who may have ruled Egypt at the end of the 4th Dynasty. From her tomb at Giza.',
        'artifact_type': 'Diorite Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/khentkawes.jpg',
        'images': ['/static/images/khentkawes_1.jpg']
    },
    {
        'id': 37,
        'name': 'Bust of Ramesses II',
        'museum': 'Museo Egizio',
        'city': 'Turin',
        'country': 'Italy',
        'latitude': 45.0684,
        'longitude': 7.6843,
        'status': 'Contested',
        'year_taken': 1824,
        'description': 'Granite bust of the great pharaoh Ramesses II, part of the extensive Drovetti collection acquired in the early 19th century.',
        'artifact_type': 'Granite Bust',
        'current_location': 'Museo Egizio, Turin',
        'image_url': '/static/images/ramesses_turin.jpg',
        'images': ['/static/images/ramesses_2.jpg']
    },
    {
        'id': 38,
        'name': 'Mummy of Ramesses I',
        'museum': 'Luxor Museum',
        'city': 'Luxor',
        'country': 'Egypt',
        'latitude': 25.6872,
        'longitude': 32.6396,
        'status': 'Returned',
        'year_taken': 1861,
        'description': 'Mummy of the founder of the 19th Dynasty. Was in the Niagara Falls Museum until identified and returned to Egypt in 2003.',
        'artifact_type': 'Royal Mummy',
        'current_location': 'Luxor Museum, Egypt',
        'image_url': '/static/images/ramesses_i.jpg',
        'images': ['/static/images/ramesses_i_1.jpg']
    },
    {
        'id': 39,
        'name': 'Statue of Sobek',
        'museum': 'Louvre Museum',
        'city': 'Paris',
        'country': 'France',
        'latitude': 48.8606,
        'longitude': 2.3376,
        'status': 'Contested',
        'year_taken': 1823,
        'description': 'Granite statue of the crocodile god Sobek, worshipped particularly in the Faiyum region. From the temple at Kom Ombo.',
        'artifact_type': 'Granite Statue',
        'current_location': 'Louvre Museum, Paris',
        'image_url': '/static/images/sobek.jpg',
        'images': ['/static/images/sobek_1.jpg']
    },
    {
        'id': 40,
        'name': 'Golden Mask of Psusennes I',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1940,
        'description': 'Solid gold funeral mask of Pharaoh Psusennes I, discovered in his intact tomb at Tanis. Often compared to Tutankhamun\'s mask.',
        'artifact_type': 'Golden Mask',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/psusennes_mask.jpg',
        'images': ['/static/images/psusennes_1.jpg']
    },
    {
        'id': 41,
        'name': 'Statue of Djoser',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1924,
        'description': 'Life-sized seated statue of Pharaoh Djoser, builder of the Step Pyramid at Saqqara. Found in the serdab of his pyramid complex.',
        'artifact_type': 'Limestone Statue',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/djoser.jpg',
        'images': ['/static/images/djoser_1.jpg']
    },
    {
        'id': 42,
        'name': 'Sarcophagus of Alexander the Great',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1801,
        'description': 'Elaborate sarcophagus believed made for Alexander the Great but used for Pharaoh Nectanebo II. From the cemetery at Sidon.',
        'artifact_type': 'Marble Sarcophagus',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/alexander_sarcophagus.jpg',
        'images': ['/static/images/alexander_1.jpg']
    },
    {
        'id': 43,
        'name': 'Statue of Thutmose III',
        'museum': 'Kunsthistorisches Museum',
        'city': 'Vienna',
        'country': 'Austria',
        'latitude': 48.2039,
        'longitude': 16.3617,
        'status': 'Contested',
        'year_taken': 1912,
        'description': 'Granite statue of the "Napoleon of Egypt," Thutmose III, known for his military campaigns that expanded the Egyptian empire.',
        'artifact_type': 'Granite Statue',
        'current_location': 'Kunsthistorisches Museum, Vienna',
        'image_url': '/static/images/thutmose_iii.jpg',
        'images': ['/static/images/thutmose_1.jpg']
    },
    {
        'id': 44,
        'name': 'Mastaba of Ka-ni-Nisut',
        'museum': 'Kunsthistorisches Museum',
        'city': 'Vienna',
        'country': 'Austria',
        'latitude': 48.2039,
        'longitude': 16.3617,
        'status': 'Contested',
        'year_taken': 1912,
        'description': 'Complete tomb chapel from the Old Kingdom period with detailed reliefs showing daily life and offering scenes.',
        'artifact_type': 'Tomb Chapel',
        'current_location': 'Kunsthistorisches Museum, Vienna',
        'image_url': '/static/images/ka_ni_nisut.jpg',
        'images': ['/static/images/mastaba_1.jpg']
    },
    {
        'id': 45,
        'name': 'Statue of Meritamen',
        'museum': 'Museo Egizio',
        'city': 'Turin',
        'country': 'Italy',
        'latitude': 45.0684,
        'longitude': 7.6843,
        'status': 'Contested',
        'year_taken': 1824,
        'description': 'Granite statue of Princess Meritamen, daughter of Ramesses II and Nefertari. Shows her in the role of a chantress of Amun.',
        'artifact_type': 'Granite Statue',
        'current_location': 'Museo Egizio, Turin',
        'image_url': '/static/images/meritamen.jpg',
        'images': ['/static/images/meritamen_1.jpg']
    },
    {
        'id': 46,
        'name': 'Sphinx of Amenemhat III',
        'museum': 'Louvre Museum',
        'city': 'Paris',
        'country': 'France',
        'latitude': 48.8606,
        'longitude': 2.3376,
        'status': 'Contested',
        'year_taken': 1823,
        'description': 'Granite sphinx with the features of Pharaoh Amenemhat III, known for his extensive building projects including the Labyrinth.',
        'artifact_type': 'Granite Sphinx',
        'current_location': 'Louvre Museum, Paris',
        'image_url': '/static/images/amenemhat_sphinx.jpg',
        'images': ['/static/images/amenemhat_1.jpg']
    },
    {
        'id': 47,
        'name': 'Statue of Intef II',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1835,
        'description': 'Sandstone statue of Pharaoh Intef II, a ruler of the 11th Dynasty who fought to reunify Egypt during the First Intermediate Period.',
        'artifact_type': 'Sandstone Statue',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/intef_ii.jpg',
        'images': ['/static/images/intef_1.jpg']
    },
    {
        'id': 48,
        'name': 'Coffin of Ipi',
        'museum': 'Egyptian Museum of Cairo',
        'city': 'Cairo',
        'country': 'Egypt',
        'latitude': 30.0478,
        'longitude': 31.2333,
        'status': 'In Egypt',
        'year_taken': 1915,
        'description': 'Elaborate Middle Kingdom coffin of the steward Ipi, decorated with Coffin Texts and offering formulas to ensure his afterlife.',
        'artifact_type': 'Wooden Coffin',
        'current_location': 'Egyptian Museum, Cairo',
        'image_url': '/static/images/ipi_coffin.jpg',
        'images': ['/static/images/ipi_1.jpg']
    },
    {
        'id': 49,
        'name': 'Statue of Senenmut with Neferure',
        'museum': 'British Museum',
        'city': 'London',
        'country': 'United Kingdom',
        'latitude': 51.5194,
        'longitude': -0.1270,
        'status': 'Contested',
        'year_taken': 1837,
        'description': 'Statue showing Senenmut, architect and royal advisor to Hatshepsut, holding Princess Neferure in a protective embrace.',
        'artifact_type': 'Granite Statue',
        'current_location': 'British Museum, London',
        'image_url': '/static/images/senenmut.jpg',
        'images': ['/static/images/senenmut_1.jpg']
    },
    {
        'id': 50,
        'name': 'Temple of Debod',
        'museum': 'Madrid',
        'city': 'Madrid',
        'country': 'Spain',
        'latitude': 40.4240,
        'longitude': -3.7175,
        'status': 'Contested',
        'year_taken': 1968,
        'description': 'Ancient Egyptian temple originally located near Aswan. Dismantled and rebuilt in Madrid as gratitude for Spanish help saving Abu Simbel.',
        'artifact_type': 'Sandstone Temple',
        'current_location': 'Madrid, Spain',
        'image_url': '/static/images/debod_temple.jpg',
        'images': ['/static/images/debod_1.jpg', '/static/images/debod_2.jpg']
    }
]
def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running in compiled bundle (APK)
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path
    
app = Flask(__name__,
            template_folder=os.path.join(get_base_path(), 'Templates'),
            static_folder=os.path.join(get_base_path(), 'static'))

# AI Assistant responses (keeping for future use)
AI_RESPONSES = {
    "greeting": ["Hello! I'm your Egyptian Artifacts assistant. How can I help you explore today?"],
    # ... other AI responses remain the same
}

@app.route('/')
def index():
    try:
        return render_template('index.html', artifacts=REAL_ARTIFACTS)
    except Exception as e:
        return f"Error loading template: {str(e)}"
    
@app.route('/map')
def map_page():
    return render_template('map.html', artifacts=REAL_ARTIFACTS)

@app.route('/api/artifacts')
def get_artifacts():
    return jsonify(REAL_ARTIFACTS)

@app.route('/artifacts')
def artifacts_list():
    countries = list(set(artifact['country'] for artifact in REAL_ARTIFACTS))
    return render_template('artifacts.html', artifacts=REAL_ARTIFACTS, countries=countries)

@app.route('/artifact/<int:artifact_id>')
def artifact_detail(artifact_id):
    artifact = next((a for a in REAL_ARTIFACTS if a['id'] == artifact_id), None)
    if artifact:
        return render_template('artifact_detail.html', artifact=artifact)
    else:
        return "Artifact not found", 404

@app.route('/statistics')
def statistics():
    total_artifacts = len(REAL_ARTIFACTS)
    contested_count = len([a for a in REAL_ARTIFACTS if a['status'] == 'Contested'])
    returned_count = len([a for a in REAL_ARTIFACTS if a['status'] == 'Returned'])
    in_egypt_count = len([a for a in REAL_ARTIFACTS if a['status'] == 'In Egypt'])
    
    countries = {}
    for artifact in REAL_ARTIFACTS:
        countries[artifact['country']] = countries.get(artifact['country'], 0) + 1
    
    country_names = list(countries.keys())
    country_counts = list(countries.values())
    
    return render_template('statistics.html', 
                         total_artifacts=total_artifacts,
                         contested_count=contested_count,
                         returned_count=returned_count,
                         in_egypt_count=in_egypt_count,
                         countries=countries,
                         country_names=country_names,
                         country_counts=country_counts)

@app.route('/api/ai-assistant', methods=['POST'])
def ai_assistant():
    user_message = request.json.get('message', '').lower()
    response = generate_ai_response(user_message)
    suggestions = get_suggestions(user_message)
    
    return jsonify({
        'response': response,
        'suggestions': suggestions
    })

def generate_ai_response(message):
    if any(word in message for word in ['hello', 'hi', 'hey']):
        return random.choice(AI_RESPONSES["greeting"])
    return "I'm here to help you explore Egyptian artifacts worldwide!"

def get_suggestions(message):
    return ["How many artifacts are there?", "Where are most artifacts located?", "Tell me about famous artifacts"]

@app.route('/static/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)

@app.route('/api/artifact/<int:artifact_id>')
def get_artifact(artifact_id):
    artifact = next((a for a in REAL_ARTIFACTS if a['id'] == artifact_id), None)
    if artifact:
        return jsonify(artifact)
    else:
        return jsonify({'error': 'Artifact not found'}), 404

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'artifacts_count': len(REAL_ARTIFACTS),
        'countries_represented': len(set(a['country'] for a in REAL_ARTIFACTS))
    })

if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)
    
    print("🏺 Egyptian Artifacts Tracker Starting...")
    print(f"📊 Total artifacts: {len(REAL_ARTIFACTS)}")
    print(f"🌍 Countries represented: {len(set(a['country'] for a in REAL_ARTIFACTS))}")
    print(f"⚖️ Contested artifacts: {len([a for a in REAL_ARTIFACTS if a['status'] == 'Contested'])}")
    print(f"✅ Returned artifacts: {len([a for a in REAL_ARTIFACTS if a['status'] == 'Returned'])}")
    print(f"🏠 Artifacts in Egypt: {len([a for a in REAL_ARTIFACTS if a['status'] == 'In Egypt'])}")
    print("🌐 Starting Flask server...")
    
    
    app.run(host='0.0.0.0', port=5000, debug=True)
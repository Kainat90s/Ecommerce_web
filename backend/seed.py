import sys
import datetime
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Product, Review

# Seed data definition
PRODUCTS_SEED = [
  {
    "id": 1,
    "name": "Aura SoundScape Pro",
    "tagline": "Silence defined. Sound refined.",
    "price": 349.99,
    "category": "Headphones",
    "rating": 4.5,
    "reviews_count": 2,
    "image": "/images/soundscape_pro.webp",
    "description": "Experience audio in its purest form. The Aura SoundScape Pro combines hybrid active noise cancellation with custom-engineered 40mm dynamic drivers to deliver a studio-grade listening experience wherever you are. Crafted with carbon fiber details and plush memory foam earcups.",
    "specs": {
      "Battery Life": "Up to 45 Hours (ANC Off)",
      "Driver Size": "40mm Bio-Cellulose",
      "Connectivity": "Bluetooth 5.3 & Ultra-Low Latency Wireless",
      "Noise Cancelling": "Hybrid ANC (up to 42dB reduction)"
    },
    "features": [
      "Hybrid Active Noise Cancellation",
      "High-Resolution Audio Certified",
      "Ultra-soft Protein Leather Cushions",
      "Smart Touch Gestures & Voice Assistant"
    ],
    "reviews": [
      {
        "name": "Sarah Jenkins",
        "rating": 5,
        "comment": "The ANC is absolute wizardry! I wear these on my daily train commute and the entire world just vanishes. Sound quality is incredibly detailed."
      },
      {
        "name": "Marcus Chen",
        "rating": 4,
        "comment": "Super comfortable for long coding sessions. The highs are crisp, though the bass is slightly boosted (which I actually like)."
      }
    ]
  },
  {
    "id": 2,
    "name": "Aura Echo Buds",
    "tagline": "Invisible fit. Indelible sound.",
    "price": 189.99,
    "category": "Earbuds",
    "rating": 5.0,
    "reviews_count": 1,
    "image": "/images/echo_buds.webp",
    "description": "Ultra-lightweight wireless earbuds that sit perfectly in your ear. The Echo Buds offer crystal-clear call quality through triple-mic arrays and rich, adaptive equalizer algorithms that tune music to your ear canal shape dynamically.",
    "specs": {
      "Battery Life": "8 Hours (28 Hours with Case)",
      "Water Resistance": "IPX7 Sweat & Water Proof",
      "Connectivity": "Bluetooth 5.3, Dual Device Connect",
      "Weight": "4.8g per earbud"
    },
    "features": [
      "Adaptive EQ Dynamic Tuning",
      "IPX7 Water & Sweat Resistance",
      "Triple-Microphone Clear Calls",
      "Sleek Glassmorphic Charging Case"
    ],
    "reviews": [
      {
        "name": "Elena Rostova",
        "rating": 5,
        "comment": "They literally don't fall out! I've been running and doing HIIT workouts with these, and they stay rock solid. Case looks futuristic."
      }
    ]
  },
  {
    "id": 3,
    "name": "Aura Horizon Frames",
    "tagline": "See clearly. Hear secretly.",
    "price": 229.99,
    "category": "Accessories",
    "rating": 5.0,
    "reviews_count": 1,
    "image": "/images/horizon_frames.webp",
    "description": "Premium polarized smart audio glasses featuring open-ear directional sound technology. Stay connected to your calls, music, and voice assistants while protecting your eyes and maintaining situational awareness.",
    "specs": {
      "Battery Life": "Up to 6 Hours Playtime",
      "Lenses": "UVA/UVB 99% Polarized Lenses",
      "Weight": "46g (Ultra-Light Frame)",
      "Audio": "Dual Directional Micro-Speakers"
    },
    "features": [
      "Open-Ear Sound System",
      "Polarized UVA/UVB Protection",
      "Touch Swipe Volume Control",
      "IPX4 Splash-Resistant Coating"
    ],
    "reviews": [
      {
        "name": "David Miller",
        "rating": 5,
        "comment": "Perfect for cycling. I can listen to my podcasts and still hear cars coming up behind me. Very stylish, looks like premium designer shades."
      }
    ]
  },
  {
    "id": 4,
    "name": "Aura Pulse Speaker",
    "tagline": "Ambient sound. Radiant atmosphere.",
    "price": 299.99,
    "category": "Accessories",
    "rating": 5.0,
    "reviews_count": 1,
    "image": "/images/pulse_speaker.webp",
    "description": "An elegant, 360-degree home smart speaker encased in high-transparency borosilicate glass. Features an integrated organic LED filament that pulses and flows in harmony with your music, casting warm glow patterns across the room.",
    "specs": {
      "Output Power": "40W Room-Filling Audio",
      "Lighting": "Full RGB Dynamic OLED Filament",
      "Battery Life": "Up to 12 Hours Portable Use",
      "Connectivity": "Wi-Fi & Bluetooth 5.2"
    },
    "features": [
      "360-Degree Omnidirectional Sound",
      "Music-Sync Ambient Light Display",
      "Premium Glassmorphic Craftsmanship",
      "Stereo Pairing Support"
    ],
    "reviews": [
      {
        "name": "Liam Anderson",
        "rating": 5,
        "comment": "This is a piece of art! The way the light pulses is so relaxing, and the sound fills my whole studio apartment. Guests always ask about it."
      }
    ]
  },
  {
    "id": 5,
    "name": "Aura Onyx Earbuds",
    "tagline": "Luxury in black. Power in sound.",
    "price": 249.99,
    "category": "Earbuds",
    "rating": 5.0,
    "reviews_count": 1,
    "image": "/images/onyx_buds.webp",
    "description": "An exquisite limited edition of our true wireless line. Features real obsidian stone details, graphene-coated audio drivers for unmatched transient speed, and premium noise isolation that lets you isolate the micro-details of symphonies.",
    "specs": {
      "Battery Life": "9 Hours (36 Hours with Case)",
      "Driver Type": "Graphene Dynamic Driver",
      "Codec": "LDAC, aptX Adaptive & AAC",
      "Finish": "Polished Obsidian & Matte Graphene"
    },
    "features": [
      "Graphene Drivers for Crystal Details",
      "High-Res LDAC Codec Support",
      "Obsidian Stone Touch Panels",
      "Wireless Qi Fast Charging Case"
    ],
    "reviews": [
      {
        "name": "Anya Vance",
        "rating": 5,
        "comment": "Audiophile grade earbuds. I didn't think wireless earbuds could sound this good. The clarity is jaw-dropping."
      }
    ]
  },
  {
    "id": 6,
    "name": "Aura SoundWave Studio",
    "tagline": "The professional benchmark.",
    "price": 499.99,
    "category": "Headphones",
    "rating": 5.0,
    "reviews_count": 1,
    "image": "/images/soundwave_studio.webp",
    "description": "Designed for studio professionals, music producers, and discerning audiophiles. Featuring open-back acoustic housing, neodymium magnets, and a massive soundstage that accurately reproduces instrument placements with micro-detail precision.",
    "specs": {
      "Frequency Response": "5Hz - 48kHz",
      "Impedance": "150 Ohms (Requires Amp for Best Performance)",
      "Acoustic Design": "Open-Back Circumaural",
      "Driver": "50mm Neodymium Planar Magnetic"
    },
    "features": [
      "Open-Back Spatial Acoustic Stage",
      "Planar Magnetic Neodymium Drivers",
      "Detachable Silver-Core OFC Cable",
      "Velvet-Soft Breathable Cushions"
    ],
    "reviews": [
      {
        "name": "Takahiro Sato",
        "rating": 5,
        "comment": "Absolutely phenomenal soundstage. I mix and master music on these, and they are incredibly flat and revealing. High price, but worth every single penny."
      }
    ]
  }
]

def seed_database():
    print("Connecting to PostgreSQL and dropping/recreating tables...")
    try:
        # Create all tables dynamically (drop old ones if exist to refresh seed)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("\n" + "="*60, file=sys.stderr)
        print("DATABASE ERROR: Could not connect to PostgreSQL or build tables.", file=sys.stderr)
        print("Please ensure:", file=sys.stderr)
        print("1. PostgreSQL service is running on your machine.", file=sys.stderr)
        print("2. You have created an empty database named 'aura_db' in pgAdmin 4.", file=sys.stderr)
        print("3. Your connection credentials in database.py are correct.", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

    db: Session = SessionLocal()
    try:
        print("Inserting AURA Audio premium products and reviews...")
        for p_data in PRODUCTS_SEED:
            reviews_data = p_data.pop("reviews", [])
            
            # Create product instance
            product = Product(**p_data)
            db.add(product)
            db.flush()  # Flushes to db to generate product.id
            
            # Insert child reviews
            for r_data in reviews_data:
                review = Review(
                    product_id=product.id,
                    name=r_data["name"],
                    rating=r_data["rating"],
                    comment=r_data["comment"],
                    date=datetime.date.today() - datetime.timedelta(days=int(p_data["id"]) * 2)
                )
                db.add(review)
                
        db.commit()
        print("Database successfully seeded with 6 luxury items!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}", file=sys.stderr)
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

from TEAMZYRO import user_collection, app as shivuu

# Rarity map

from pyrogram import enums

from TEAMZYRO import bounty_values, rarity_map

from pyrogram import Client, filters
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
import io
from pyrogram import enums

from PIL import Image
import io
import os

async def fetch_and_resize_profile_photo(client, user_id):
    # Fetch photos using the async generator
    photos = []
    async for photo in client.get_chat_photos(user_id):
        photos.append(photo)

    if not photos:
        raise ValueError("No profile photos found for the user.")

    # Download the first photo
    temp_file_path = await client.download_media(photos[0].file_id)
    
    # Read the file content as bytes
    with open(temp_file_path, "rb") as file:
        file_content = file.read()

    # Open the file content as an Image
    with Image.open(io.BytesIO(file_content)) as img:
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="PNG")
        img_byte_array.seek(0)

    # Cleanup the temporary file
    os.remove(temp_file_path)

    return img_byte_array

from PIL import Image, ImageDraw, ImageFont
import io
from PIL import Image, ImageDraw, ImageFont
import io

async def create_wanted_poster(name: str, total_bounty: int, total_chars: int, rarity_breakdown: str, profile_image=None):
    # Open the template image
    template = Image.open("wanted_template.jpg")
    draw = ImageDraw.Draw(template)

    # Load fonts
    try:
        playfair_font_path = "PlayfairDisplay-Bold.ttf"  # Path to the Playfair Display font file
        noto_sans_font_path = "NotoSans-Regular.ttf"  # Path to the Noto Sans Regular font file for name
        
        name_font_size = 250  # Increased name font size
        bounty_font_size = 200  # Increased bounty font size
        
        name_font = ImageFont.truetype(noto_sans_font_path, name_font_size)  # Use NotoSans for name
        bounty_font = ImageFont.truetype(playfair_font_path, bounty_font_size)
    except:
        name_font = ImageFont.load_default()
        bounty_font = ImageFont.load_default()

    # Add profile image with a black border
    if profile_image:
        profile_image = profile_image.resize((720, 510), Image.Resampling.LANCZOS)
        
        # Create a new image with a black border around the profile image
        border_size = 4
        bordered_image = Image.new("RGBA", (profile_image.width + 2 * border_size, profile_image.height + 2 * border_size), "black")
        bordered_image.paste(profile_image, (border_size, border_size))
        
        # Paste the bordered image onto the template
        template.paste(bordered_image, (40, 280))

    # Define colors
    text_color = "#4A2511"  # Dark brown color
    bg_color = "#f4e4bc"    # Light beige background (adjust template if needed)

    # Add name
    name_area = (90, 900, 740, 1040)
    name_width = draw.textlength(name, font=name_font)
    name_height = name_font.size
    while name_width > (name_area[2] - name_area[0]) or name_height > (name_area[3] - name_area[1]):
        name_font_size -= 5
        name_font = ImageFont.truetype(noto_sans_font_path, name_font_size)  # Re-load with adjusted size
        name_width = draw.textlength(name, font=name_font)
        name_height = name_font.size

    name_x = (name_area[2] + name_area[0] - name_width) // 2
    name_y = (name_area[3] + name_area[1] - name_height) // 2 - 20  # Move 20px up
    draw.text((name_x, name_y), name, fill=text_color, font=name_font)

    # Add bounty
    bounty_text = f"{total_bounty:,}"
    bounty_area = (160, 1060, 760, 1120)
    bounty_width = draw.textlength(bounty_text, font=bounty_font)
    bounty_height = bounty_font.size
    while bounty_width > (bounty_area[2] - bounty_area[0]) or bounty_height > (bounty_area[3] - bounty_area[1]):
        bounty_font_size -= 5
        bounty_font = ImageFont.truetype(playfair_font_path, bounty_font_size)
        bounty_width = draw.textlength(bounty_text, font=bounty_font)
        bounty_height = bounty_font.size

    bounty_x = 160
    bounty_y = (bounty_area[3] + bounty_area[1] - bounty_height) // 2 - 20  # Move 20px up
    draw.text((bounty_x, bounty_y), bounty_text, fill=text_color, font=bounty_font)

    img_byte_array = io.BytesIO()
    template.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return img_byte_array



async def mybounty(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Fetch user data from MongoDB
    user = await user_collection.find_one({'id': user_id})
    if not user:
        await message.reply_text("You have no characters, so no bounty for now. Start collecting!")
        return

    # Calculate bounties
    total_bounty = 0
    rarity_counts = {key: 0 for key in rarity_map.keys()}
    rarity_lookup = {value: key for key, value in rarity_map.items()}
    
    
    for character in user['characters']:
        rarity = character.get('rarity')
        rarity_key = rarity_lookup.get(rarity, 1)
        rarity_counts[rarity_key] += 1
        total_bounty += bounty_values.get(rarity_key, 100)

    rarity_breakdown = "\n".join(
        f"{rarity_map[rarity]}: {count}" 
        for rarity, count in rarity_counts.items() 
        if count > 0
    )

    # Fetch profile image (no resizing)
    profile_image = await fetch_and_resize_profile_photo(client, user_id)

    # Generate the wanted poster
    poster_image = await create_wanted_poster(
        name=message.from_user.first_name,
        total_bounty=total_bounty,
        total_chars=len(user['characters']),
        rarity_breakdown=rarity_breakdown,
        profile_image=Image.open(profile_image) if profile_image else None
    )

    # Send the image with caption
    caption = f"🏴‍☠️ <b>{message.from_user.first_name}'s Bounty Report</b>\n\n{rarity_breakdown}"
    await message.reply_photo(
        photo=poster_image,
        caption=caption,
        parse_mode=enums.ParseMode.HTML
    )


@shivuu.on_message(filters.command("bounty"))
async def mybounty_handler(client: Client, message: Message):
    await mybounty(client, message)
  

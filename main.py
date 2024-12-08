import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import os

# ตั้งค่าบอท
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# รายชื่อบ้านพร้อม ID บทบาทและคำอธิบาย
houses = {
    "Celestial Ridge": {
        "id": 1315256958952935474,
        "color": "สีฟ้า",
        "description": (
            "Celestial Ridge (เซ-เลส-เทียล ริดจ์)\n"
            '"ความกล้าหาญเป็นแสงสว่างที่นำทางหัวใจ หากเจ้าเต็มไปด้วยพลังที่จะเผชิญหน้ากับความท้าทายและความมืด บ้านแห่งแสงจะเป็นที่ที่เจ้าเรียกว่าบ้าน!"'
        )
    },
    "Astro Haven": {
        "id": 1315257066579038219,
        "color": "สีทอง",
        "description": (
            "Astro Haven (แอส-โตร เฮเว่น)\n"
            '"ปัญญาและการมองเห็นเป็นอาวุธที่ทรงพลัง หากเจ้ามีสายตาที่มองผ่านหมู่ดาวและจิตใจที่แสวงหาความจริง บ้านแห่งดาราจะต้อนรับเจ้าอย่างอบอุ่น!"'
        )
    },
    "Nebulon": {
        "id": 1315257140151193721,
        "color": "สีม่วง",
        "description": (
            "Nebulon (เนบ-ยู-ลอน)\n"
            '"ในหมอกที่ซ่อนเร้น การปรับตัวคือกุญแจสู่ความอยู่รอด หากเจ้าเชี่ยวชาญในศิลปะแห่งการปรับตัวและหลีกเลี่ยงภัยอันตราย บ้านแห่งหมอกจะเป็นที่พำนักของเจ้า!"'
        )
    }
}

# ห้อง log, ห้องเลือกบ้านและห้องแจ้งผล
LOG_CHANNEL_ID = 1293963040391303290
CHOSE_HOUSE_CHANNEL_ID = 1315328457013461113
HOUSE_CHANNEL_ID = 1315328734794092544

# ฟังก์ชันสุ่มบ้าน
def select_house():
    return random.choice(list(houses.keys()))

# คำสั่ง !house พร้อมปุ่ม
@bot.command()
async def house(ctx):
    button = Button(label="สุ่มบ้าน", style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        house_name = select_house()
        house_info = houses[house_name]
        role_id = house_info["id"]
        role = ctx.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message(f"ไม่พบบทบาท {house_name} ในเซิร์ฟเวอร์!", ephemeral=True)
            return

        # ลบบทบาทบ้านเก่า (ถ้ามี)
        for old_role in interaction.user.roles:
            if old_role.id in [info["id"] for info in houses.values()]:
                await interaction.user.remove_roles(old_role)

        # เพิ่มบทบาทบ้านใหม่
        await interaction.user.add_roles(role)

        # ส่งข้อความ log ไปยังห้อง log
        log_channel = ctx.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"**{interaction.user}** ถูกสุ่มเลือกให้อยู่บ้าน **{house_name}** ({house_info['color']})."
            )

        # ส่งข้อความไปยังช่องแจ้งผล
        house_channel = ctx.guild.get_channel(HOUSE_CHANNEL_ID)
        if house_channel:
            await house_channel.send(
                f"{interaction.user.mention} ถูกสุ่มเลือกให้อยู่บ้าน **{house_name}** ({house_info['color']})!\n\n"
                f"{house_info['description']}"
            )

        await interaction.response.send_message("การเลือกบ้านสำเร็จแล้ว!", ephemeral=True)

    button.callback = button_callback
    view = View()
    view.add_item(button)
    await ctx.send("กดปุ่มเพื่อสุ่มบ้านของคุณ!", view=view)

@bot.event
async def on_ready():
    print(f"บอท {bot.user} พร้อมใช้งาน!")

# รันบอท
bot.run(os.getenv("DISCORD_TOKEN"))

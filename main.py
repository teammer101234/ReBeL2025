import discord
from discord.ext import commands
from discord import app_commands

from webserver import server_on

TOKEN = "MTMxMzQ0Mjc2ODg1NjY3ODQyMw.G8tNXc.ib6-cDWsANq-X6WrrYsD0MegrU0twypRTPTSVI"  # ใส่โทเค็นของบอท
GUILD_ID = 1313472193119916044  # ใส่ ID ของเซิร์ฟเวอร์คุณ
ROLE_MAPPING = {
    "RuneKnight": 1342538983971754137,
    "RoyalGuard": 1342539093879554178,
    "Warlock": 1342539188347732020,
    "Sorcerer": 1342539293075439636,
    "Guillotine": 1342539378060300350,
    "ShadowChaser": 1342539434502918156,
    "Ranger": 1342539504044736583,
    "Wanderer": 1342539743950405662,
    "Minstrel": 1342539820265635840,
    "Archbishop": 1342539904059707402,
    "Shura": 1342540005263937578,
    "Mechanic": 1342540096028807220,
    "Genetic": 1342540159358468207
}  # ใส่ ID ของ Role แต่ละอาชีพ

# ตั้งค่าบอท
intents = discord.Intents.default()
intents.members = True  # ให้บอทสามารถเปลี่ยนชื่อสมาชิกได้
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- ฟอร์ม Verify ---- #
class VerifyForm(discord.ui.Modal, title="Verify ตัวละครของคุณ"):
    real_name = discord.ui.TextInput(label="ชื่อเล่น", placeholder="ชื่อของคุณ", required=True)
    character_name = discord.ui.TextInput(label="ชื่อตัวละคร", placeholder="ชื่อในเกม", required=True)
    main_class = discord.ui.TextInput(label="อาชีพหลัก", placeholder="RuneKnight, RuneKnight, Warlock, Sorcerer...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        real_name = self.real_name.value.strip()
        character_name = self.character_name.value.strip()
        main_class = self.main_class.value.strip()

        # ตรวจสอบว่าอาชีพที่พิมพ์มามี Role หรือไม่
        role_id = ROLE_MAPPING.get(main_class)
        if not role_id:
            await interaction.response.send_message("❌  อาชีพที่ระบุไม่มีในระบบ! โปรดตรวจสอบอีกครั้ง", ephemeral=True)
            return

        # เปลี่ยนชื่อใน Discord
        new_nickname = f"({real_name}) {character_name} [{main_class}]"
        try:
            await interaction.user.edit(nick=new_nickname)
        except discord.Forbidden:
            await interaction.response.send_message("❌  บอทไม่มีสิทธิ์เปลี่ยนชื่อ!", ephemeral=True)
            return

        # ให้ Role ตามอาชีพ
        role = interaction.guild.get_role(role_id)
        if role:
            await interaction.user.add_roles(role)

        await interaction.response.send_message(f"✅ ยืนยันตัวตนสำเร็จ! ชื่อของคุณถูกเปลี่ยนเป็น `{new_nickname}` และได้รับอาชีพ `{main_class}`เรียบร้อยแล้ว", ephemeral=True)

# ---- ปุ่มสำหรับกด "ยืนยันตัวตน" ---- #
class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ยืนยันตัวตน", style=discord.ButtonStyle.primary, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(VerifyForm())

# ---- คำสั่งสำหรับตั้งค่า Embed Verify ---- #
@bot.tree.command(name="setup_verify", description="ตั้งค่า Embed สำหรับการยืนยันตัวตน")
@commands.has_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)  # ตรวจสอบว่าเป็นแอดมิน
async def setup_verify(interaction: discord.Interaction):
    embed = discord.Embed(
        title="┌───⋅≪ Welcome to ReBeL ≫⋅ ───┐",
        description="กดปุ่ม **'ยืนยันตัวตน'** พื่อกรอกข้อมูลของคุณ\n"
                    " **'พิมพ์อาชีพให้ถูกต้องตามที่แจ้งดังนี้'** \n"
                    " <:RuneKnight:1342531450167234584>           ➤        RuneKnight\n"
                    " <:RoyalGuard:1342531448242049024>           ➤        RoyalGuard\n"
                    " <:Warlock:1342531439165575362>           ➤        Warlock\n"
                    " <:Sorcerer:1342531462150492240>           ➤        Sorcerer\n"
                    " <:GuillotineCross:1342535934058561606>           ➤        Guillotine\n"
                    " <:ShadowChaser:1342531452251934761>           ➤        ShadowChaser\n"
                    " <:Ranger:1342531445566214175>           ➤        Ranger\n"
                    " <:Wanderer:1342531464511885494>           ➤        Wanderer\n"
                    " <:Minstrel:1342531443859132416>           ➤        Minstrel\n"
                    " <:Archbishop:1342535936516558949>           ➤        Archbishop\n"
                    " <:Shura:1342531459185115198>           ➤        Shura\n"
                    " <:Mechanic:1342531441711644733>           ➤        Mechanic\n"
                    " <:Genetic:1342535938949255218>           ➤        Genetic\n",
        color=discord.Color.blue()
    )
    embed.set_footer(text="⚔ ระบบยืนยันตัวตนของเซิร์ฟเวอร์ ⚔")
    
    await interaction.channel.send(embed=embed, view=VerifyButton())
    await interaction.response.send_message("✅ ตั้งค่า Embed สำเร็จ!", ephemeral=True)

# ---- Event เมื่อบอทพร้อม ---- #
@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้ว: {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        print("✅ ซิงค์ Slash Commands สำเร็จ!")
    except Exception as e:
        print(f"❌ พบข้อผิดพลาดในการซิงค์คำสั่ง: {e}")

server_on()
# ---- รันบอท ---- #
bot.run(TOKEN)

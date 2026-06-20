const { Telegraf } = require('telegraf');
const express = require('express');

// التأكد من وجود التوكن
if (!process.env.BOT_TOKEN) {
    console.error('Error: BOT_TOKEN is not defined in environment variables!');
    process.exit(1);
}

const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();

app.use(express.json());

// مسار لاستقبال التنبيهات من لعبتك
// الرابط سيكون: https://sab3-ai-bot.onrender.com/notify
app.post('/notify', async (req, res) => {
    const { msg } = req.body;
    
    if (!msg) {
        return res.status(400).send('Message content is missing');
    }

    try {
        await bot.telegram.sendMessage(process.env.ADMIN_ID, `🤖 تنبيه من لعبة Bot al-Sabaa: \n\n${msg}`);
        res.status(200).send('Message sent to Telegram!');
    } catch (e) {
        console.error('Telegram Error:', e);
        res.status(500).send('Failed to send message');
    }
});

// تشغيل البوت
bot.launch()
    .then(() => console.log('Bot is running...'))
    .catch(err => console.error('Bot launch error:', err));

// تشغيل السيرفر
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));

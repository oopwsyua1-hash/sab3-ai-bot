const { Telegraf } = require('telegraf');
const express = require('express');

// إعدادات البوت والسيرفر
const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();

app.use(express.json());

// 1. أمر البداية (للتأكد أن البوت شغال)
bot.command('start', (ctx) => {
    ctx.reply('🚀 أهلاً بك في Bot al-Sabaa! السيرفر يعمل وجاهز لاستقبال تنبيهات اللعبة.');
});

// 2. مسار استقبال التنبيهات من اللعبة (الرابط: /notify)
app.post('/notify', async (req, res) => {
    const { msg } = req.body;
    
    if (!msg) {
        return res.status(400).send('Message content is missing');
    }

    try {
        await bot.telegram.sendMessage(process.env.ADMIN_ID, `🤖 تنبيه من لعبة Bot al-Sabaa:\n\n${msg}`);
        res.status(200).send('Message sent to Telegram!');
    } catch (e) {
        console.error('Telegram Error:', e);
        res.status(500).send('Failed to send message');
    }
});

// تشغيل البوت والسيرفر
bot.launch()
    .then(() => console.log('Bot is running...'))
    .catch(err => console.error('Bot launch error:', err));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));

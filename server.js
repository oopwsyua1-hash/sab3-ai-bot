const { Telegraf } = require('telegraf');
const express = require('express');
const cors = require('cors');

// إعداد البوت باستخدام التوكن من إعدادات Render
const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();

app.use(cors());
app.use(express.json());

// مسار للتحقق أن السيرفر يعمل
app.get('/', (req, res) => {
    res.send('Server is running and Bot is active!');
});

// المسار الذي تستقبله اللعبة
app.post('/webhook', async (req, res) => {
    const { message } = req.body;
    try {
        await bot.telegram.sendMessage(process.env.ADMIN_ID, `تنبيه من اللعبة: ${message}`);
        res.status(200).json({ status: 'success' });
    } catch (error) {
        console.error('Error sending message:', error);
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// تشغيل البوت والسيرفر
bot.launch();
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

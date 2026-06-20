const { Telegraf, Markup } = require('telegraf');
const express = require('express');

const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();
app.use(express.json());

// قاعدة بيانات مؤقتة للأرصدة (لأغراض التجربة)
const userBalances = {}; 

bot.command('start', (ctx) => {
    ctx.reply('🚀 أهلاً بك في Bot al-Sabaa! اختر من القائمة:', Markup.inlineKeyboard([
        [Markup.button.webApp('🎮 فتح اللعبة', 'https://sab3-ai-bot.onrender.com')],
        [Markup.button.callback('💰 معرفة الرصيد', 'balance')],
        [Markup.button.callback('💵 شحن رصيد', 'charge')],
        [Markup.button.callback('💸 سحب أرباح', 'withdraw')]
    ]));
});

// معرفة الرصيد
bot.action('balance', (ctx) => {
    const userId = ctx.from.id;
    const balance = userBalances[userId] || 0;
    ctx.reply(`📊 رصيدك الحالي هو: ${balance} عملة`);
});

// شحن الرصيد
bot.action('charge', (ctx) => {
    ctx.reply('لشحن الرصيد، يرجى تحويل المبلغ للإدارة ثم إرسال صورة الوصل.');
});

// سحب الأرباح
bot.action('withdraw', (ctx) => {
    ctx.reply('لطلب سحب الأرباح، يرجى كتابة المبلغ المطلوب.');
});

// استقبال تنبيهات اللعبة (إضافة رصيد تلقائي من اللعبة)
app.post('/notify', async (req, res) => {
    const { userId, amount, msg } = req.body;
    if (userId) {
        userBalances[userId] = (userBalances[userId] || 0) + (amount || 0);
    }
    await bot.telegram.sendMessage(process.env.ADMIN_ID, `تنبيه من اللعبة: ${msg || 'تم تحديث رصيد'}`);
    res.status(200).send('Done');
});

bot.launch();
app.listen(process.env.PORT || 3000);

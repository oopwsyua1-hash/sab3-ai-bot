const { Telegraf, Markup } = require('telegraf');
const express = require('express');

const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();
app.use(express.json());

// رابط الإدارة الثابت
const ADMIN_LINK = "https://t.me/Qsui123";

// أمر البداية مع القائمة الاحترافية
bot.command('start', (ctx) => {
    ctx.reply('🚀 أهلاً بك في Bot al-Sabaa!\nاختر الخدمة المطلوبة:', Markup.inlineKeyboard([
        [Markup.button.webApp('🎮 فتح اللعبة', 'https://sab3-ai-bot.onrender.com')],
        [Markup.button.callback('📊 رصيدي', 'balance')],
        [Markup.button.callback('💰 شحن رصيد', 'charge')],
        [Markup.button.callback('💸 سحب أرباح', 'withdraw')],
        [Markup.button.url('📞 تواصل مع الإدارة', ADMIN_LINK)]
    ]));
});

// قائمة الشحن
bot.action('charge', (ctx) => {
    ctx.reply('💳 اختر طريقة الشحن:', Markup.inlineKeyboard([
        [Markup.button.callback('شام كاش', 'charge_sham')],
        [Markup.button.callback('كرت بنك', 'charge_bank')],
        [Markup.button.callback('🔙 رجوع', 'start')]
    ]));
});

// قائمة السحب
bot.action('withdraw', (ctx) => {
    ctx.reply('🏦 اختر طريقة السحب:', Markup.inlineKeyboard([
        [Markup.button.callback('سحب شام كاش', 'withdraw_sham')],
        [Markup.button.callback('سحب كرت بنك', 'withdraw_bank')],
        [Markup.button.callback('🔙 رجوع', 'start')]
    ]));
});

// التعامل مع اختيارات الشحن والسحب
bot.action(/charge_.+/, (ctx) => ctx.reply(`يرجى تحويل المبلغ عبر ${ctx.match[0].split('_')[1]} ثم إرسال الوصل للإدارة هنا: ${ADMIN_LINK}`));
bot.action(/withdraw_.+/, (ctx) => ctx.reply(`يرجى كتابة المبلغ المطلوب سحبه عبر ${ctx.match[0].split('_')[1]} وسنتواصل معك.`));

// معرفة الرصيد
bot.action('balance', (ctx) => ctx.reply('📊 رصيدك الحالي هو: 0 عملة (يتم تحديثه تلقائياً)'));

// العودة للقائمة الرئيسية
bot.action('start', (ctx) => {
    ctx.editMessageText('🚀 القائمة الرئيسية:', Markup.inlineKeyboard([
        [Markup.button.webApp('🎮 فتح اللعبة', 'https://seda-alhlde.lovable.app/')],
        [Markup.button.callback('📊 رصيدي', 'balance')],
        [Markup.button.callback('💰 شحن رصيد', 'charge')],
        [Markup.button.callback('💸 سحب أرباح', 'withdraw')],
        [Markup.button.url('📞 تواصل مع الإدارة', ADMIN_LINK)]
    ]));
});

// استقبال التنبيهات
app.post('/notify', async (req, res) => {
    const { msg } = req.body;
    await bot.telegram.sendMessage(process.env.ADMIN_ID, `🤖 تنبيه: ${msg}`);
    res.status(200).send('Done');
});

bot.launch();
app.listen(process.env.PORT || 3000);

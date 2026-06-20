const { Telegraf, Markup } = require('telegraf');
const express = require('express');

// إعداد البوت
const bot = new Telegraf(process.env.BOT_TOKEN);
const app = express();
app.use(express.json());

// الرابط الثابت للعبة والإدارة
const GAME_URL = "https://lovable.dev/preview/IzX91e1HJYxfnB9X4pwAu2GNU1lghDXM";
const ADMIN_LINK = "https://t.me/Qsui123";

// أمر البداية (القائمة الرئيسية)
bot.command('start', (ctx) => {
    ctx.reply('🚀 أهلاً بك في Bot al-Sabaa!\nاختر الخدمة المطلوبة:', Markup.inlineKeyboard([
        [Markup.button.webApp('🎮 فتح اللعبة', GAME_URL)],
        [Markup.button.callback('📊 رصيدي', 'balance')],
        [Markup.button.callback('💰 شحن رصيد', 'charge')],
        [Markup.button.callback('💸 سحب أرباح', 'withdraw')],
        [Markup.button.url('📞 تواصل مع الإدارة', ADMIN_LINK)]
    ]));
});

// التعامل مع قائمة الشحن
bot.action('charge', (ctx) => {
    ctx.editMessageText('💳 اختر طريقة الشحن:', Markup.inlineKeyboard([
        [Markup.button.callback('شام كاش', 'charge_sham')],
        [Markup.button.callback('كرت بنك', 'charge_bank')],
        [Markup.button.callback('🔙 رجوع', 'start')]
    ]));
});

// التعامل مع قائمة السحب
bot.action('withdraw', (ctx) => {
    ctx.editMessageText('🏦 اختر طريقة السحب:', Markup.inlineKeyboard([
        [Markup.button.callback('سحب شام كاش', 'withdraw_sham')],
        [Markup.button.callback('سحب كرت بنك', 'withdraw_bank')],
        [Markup.button.callback('🔙 رجوع', 'start')]
    ]));
});

// التعامل مع اختيارات الشحن والسحب
bot.action(/charge_.+/, (ctx) => {
    const method = ctx.match[0].split('_')[1];
    ctx.reply(`يرجى تحويل المبلغ عبر ${method} ثم إرسال صورة الوصل للإدارة هنا: ${ADMIN_LINK}`);
});

bot.action(/withdraw_.+/, (ctx) => {
    const method = ctx.match[0].split('_')[1];
    ctx.reply(`لطلب سحب الأرباح عبر ${method}، يرجى كتابة المبلغ المطلوب وسنتواصل معك فوراً.`);
});

// معرفة الرصيد
bot.action('balance', (ctx) => ctx.reply('📊 رصيدك الحالي هو: 0 عملة.'));

// زر الرجوع للقائمة الرئيسية
bot.action('start', (ctx) => {
    ctx.editMessageText('🚀 القائمة الرئيسية:', Markup.inlineKeyboard([
        [Markup.button.webApp('🎮 فتح اللعبة', GAME_URL)],
        [Markup.button.callback('📊 رصيدي', 'balance')],
        [Markup.button.callback('💰 شحن رصيد', 'charge')],
        [Markup.button.callback('💸 سحب أرباح', 'withdraw')],
        [Markup.button.url('📞 تواصل مع الإدارة', ADMIN_LINK)]
    ]));
});

// تشغيل البوت (تم استخدام webhook إذا كنت تريد، لكن لنبقى على launch الآن)
bot.launch()
    .then(() => console.log('Bot is running...'))
    .catch((err) => console.error('Error starting bot:', err));

// تشغيل السيرفر
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}`));

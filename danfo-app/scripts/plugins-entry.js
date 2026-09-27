// Bundled into www/monetize/plugins.js by scripts/build-web.mjs so the plain-JS game can use the native plugins.
import { Capacitor } from '@capacitor/core';
import { AdMob } from '@capacitor-community/admob';
import { Purchases } from '@revenuecat/purchases-capacitor';
import { Share } from '@capacitor/share';
import { App } from '@capacitor/app';
window.DCPlugins = { Capacitor, AdMob, Purchases, Share, App, platform: Capacitor.getPlatform(), native: Capacitor.isNativePlatform() };

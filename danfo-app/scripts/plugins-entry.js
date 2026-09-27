// Bundled into www/monetize/plugins.js by scripts/build-web.mjs so the plain-JS game can use native plugins.
// Version 1.0: share + app lifecycle only. Version 1.1 adds AdMob + RevenueCat (see V1.1_MONETIZATION.md).
import { Capacitor } from '@capacitor/core';
import { Share } from '@capacitor/share';
import { App } from '@capacitor/app';
window.DCPlugins = { Capacitor, Share, App, platform: Capacitor.getPlatform(), native: Capacitor.isNativePlatform() };

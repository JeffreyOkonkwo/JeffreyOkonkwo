# Applies the Danfo Craze native settings after `npx cap add android/ios` (safe to run more than once):
# portrait only, no Android advertising ID (Families), AdMob App IDs + SKAdNetwork list.
import re, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
man_p = os.path.join(root, 'android/app/src/main/AndroidManifest.xml'); s = open(man_p).read()
if 'xmlns:tools' not in s: s = s.replace('<manifest xmlns:android="http://schemas.android.com/apk/res/android">', '<manifest xmlns:android="http://schemas.android.com/apk/res/android"\n    xmlns:tools="http://schemas.android.com/tools">')
if 'screenOrientation' not in s: s = s.replace('        <activity\n', '        <activity\n            android:screenOrientation="portrait"\n', 1)
if 'permission.AD_ID' not in s: s = s.replace('    <uses-permission android:name="android.permission.INTERNET" />', '    <uses-permission android:name="android.permission.INTERNET" />\n    <!-- Families policy: a game for children must not use the advertising ID -->\n    <uses-permission android:name="com.google.android.gms.permission.AD_ID" tools:node="remove" />')
if 'gms.ads.APPLICATION_ID' not in s: s = s.replace('        <activity\n', open(os.path.join(here, 'admob-android.xml')).read() + '\n        <activity\n', 1)
open(man_p, 'w').write(s)
pl_p = os.path.join(root, 'ios/App/App/Info.plist'); s = open(pl_p).read()
s = re.sub(r'<key>UISupportedInterfaceOrientations</key>\s*<array>.*?</array>\s*<key>UISupportedInterfaceOrientations~ipad</key>\s*<array>.*?</array>',
  '<key>UISupportedInterfaceOrientations</key>\n\t<array>\n\t\t<string>UIInterfaceOrientationPortrait</string>\n\t</array>\n\t<key>UISupportedInterfaceOrientations~ipad</key>\n\t<array>\n\t\t<string>UIInterfaceOrientationPortrait</string>\n\t\t<string>UIInterfaceOrientationPortraitUpsideDown</string>\n\t</array>', s, flags=re.S)
# no special encryption (only standard HTTPS): TestFlight/App Store then skip the export compliance question
if 'ITSAppUsesNonExemptEncryption' not in s: k = s.rindex('</dict>'); s = s[:k] + '\t<key>ITSAppUsesNonExemptEncryption</key>\n\t<false/>\n' + s[k:]
if 'GADApplicationIdentifier' not in s: k = s.rindex('</dict>'); s = s[:k] + open(os.path.join(here, 'admob-ios.plist.xml')).read() + s[k:]
open(pl_p, 'w').write(s); print('native settings applied')

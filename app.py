from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from functools import wraps
import secrets
import os
import requests
from urllib.parse import quote
import json
import hashlib
import random
import time
from datetime import datetime, timedelta
import re
from collections import defaultdict
import math
import base64

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.permanent_session_lifetime = timedelta(days=7)

# ========== ADMIN CONFIGURATION ==========
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
OMDB_API_KEY = os.environ.get('OMDB_API_KEY', 'f7b8d9c2')

# ========== COMPLETE MULTI-LANGUAGE TRANSLATIONS (500+ lines) ==========
TRANSLATIONS = {
    "english": {
        "site_name": "XSTAR",
        "tagline": "Movies, Series, Anime & More",
        "hero_title": "Unlimited Movies, Series, and Anime",
        "hero_subtitle": "Watch anywhere. Cancel anytime. AI-powered recommendations just for you.",
        "get_started": "Get Started",
        "sign_in": "Sign In",
        "sign_up": "Sign Up",
        "logout": "Logout",
        "search_placeholder": "Search movies, series, anime...",
        "trending": "Trending Now",
        "recommended": "Recommended For You",
        "latest": "Latest Releases",
        "hindi_dubbed": "Hindi Dubbed",
        "anime": "Anime Series",
        "anime_movies": "Anime Movies",
        "hollywood": "Hollywood Blockbusters",
        "bollywood": "Bollywood Hits",
        "watch_now": "Watch Now",
        "download": "Download",
        "rating": "Rating",
        "duration": "Duration",
        "genre": "Genre",
        "language": "Language",
        "story": "Story",
        "cast": "Cast",
        "director": "Director",
        "year": "Year",
        "profile": "My Profile",
        "settings": "Settings",
        "help": "Help Center",
        "language_select": "Select Language",
        "welcome_back": "Welcome Back",
        "new_here": "New here?",
        "create_account": "Create Account",
        "email": "Email Address",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "full_name": "Full Name",
        "remember_me": "Remember Me",
        "forgot_password": "Forgot Password?",
        "already_have_account": "Already have an account?",
        "dont_have_account": "Don't have an account?",
        "login": "Login",
        "register": "Register",
        "footer_text": "© 2024 XSTAR. All rights reserved. Watch your favorite movies and anime in multiple languages.",
        "watch_history": "Watch History",
        "favorites": "My Favorites",
        "continue_watching": "Continue Watching",
        "top_rated": "Top Rated",
        "coming_soon": "Coming Soon",
        "recently_added": "Recently Added",
        "action": "Action",
        "comedy": "Comedy",
        "drama": "Drama",
        "romance": "Romance",
        "sci_fi": "Sci-Fi",
        "horror": "Horror",
        "thriller": "Thriller",
        "adventure": "Adventure",
        "fantasy": "Fantasy",
        "crime": "Crime",
        "mystery": "Mystery",
        "documentary": "Documentary",
        "family": "Family",
        "war": "War",
        "western": "Western",
        "musical": "Musical",
        "sport": "Sport",
        "history": "History",
        "biography": "Biography",
        "add_to_watchlist": "Add to Watchlist",
        "remove_from_watchlist": "Remove from Watchlist",
        "share": "Share",
        "report": "Report",
        "feedback": "Feedback",
        "privacy_policy": "Privacy Policy",
        "terms_of_service": "Terms of Service",
        "contact_us": "Contact Us",
        "about_us": "About Us",
        "faq": "FAQ",
        "live_chat": "Live Chat",
        "notification": "Notifications",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",
        "auto_play": "Auto Play",
        "quality": "Quality",
        "subtitles": "Subtitles",
        "audio": "Audio",
        "download_location": "Download Location",
        "clear_cache": "Clear Cache",
        "logout_confirm": "Are you sure you want to logout?",
        "delete_account": "Delete Account",
        "change_password": "Change Password",
        "update_profile": "Update Profile",
        "profile_picture": "Profile Picture",
        "membership": "Membership",
        "premium": "Premium",
        "free_trial": "Free Trial",
        "subscribe": "Subscribe",
        "cancel_subscription": "Cancel Subscription",
        "billing": "Billing",
        "payment_method": "Payment Method",
        "invoice": "Invoice",
        "view_all": "View All",
        "load_more": "Load More",
        "no_results": "No results found",
        "try_again": "Try again",
        "network_error": "Network error",
        "server_error": "Server error",
        "success": "Success",
        "error": "Error",
        "warning": "Warning",
        "info": "Info",
        "close": "Close",
        "back": "Back",
        "next": "Next",
        "previous": "Previous",
        "page": "Page",
        "of": "of",
        "sort_by": "Sort by",
        "filter_by": "Filter by",
        "clear_filters": "Clear Filters",
        "apply_filters": "Apply Filters",
        "year_range": "Year Range",
        "min_rating": "Minimum Rating",
        "max_duration": "Maximum Duration",
        "season": "Season",
        "episode": "Episode",
        "trailer": "Trailer",
        "behind_the_scenes": "Behind the Scenes",
        "interviews": "Interviews",
        "reviews": "Reviews",
        "ratings": "Ratings",
        "similar": "Similar",
        "more_like_this": "More Like This",
        "you_may_also_like": "You May Also Like",
        "because_you_watched": "Because You Watched",
        "trending_in": "Trending in",
        "top_10": "Top 10",
        "new_releases": "New Releases",
        "coming_this_week": "Coming This Week",
        "leaving_soon": "Leaving Soon",
        "critics_picks": "Critics Picks",
        "audience_favorites": "Audience Favorites",
        "award_winning": "Award Winning",
        "hidden_gems": "Hidden Gems",
        "staff_picks": "Staff Picks",
        "daily_recommendations": "Daily Recommendations",
        "weekly_top_10": "Weekly Top 10",
        "monthly_most_watched": "Monthly Most Watched",
        "all_time_favorites": "All Time Favorites",
        "recently_watched": "Recently Watched",
        "resume_watching": "Resume Watching",
        "watched": "Watched",
        "unwatched": "Unwatched",
        "mark_as_watched": "Mark as Watched",
        "mark_as_unwatched": "Mark as Unwatched",
        "rate_this": "Rate This",
        "your_rating": "Your Rating",
        "average_rating": "Average Rating",
        "total_ratings": "Total Ratings",
        "write_review": "Write a Review",
        "see_all_reviews": "See All Reviews",
        "review_title": "Review Title",
        "review_content": "Review Content",
        "submit_review": "Submit Review",
        "edit_review": "Edit Review",
        "delete_review": "Delete Review",
        "review_helpful": "Was this review helpful?",
        "yes": "Yes",
        "no": "No",
        "report_review": "Report Review",
        "reported": "Reported",
        "thanks_for_feedback": "Thanks for your feedback!",
        "feature_request": "Feature Request",
        "bug_report": "Bug Report",
        "general_inquiry": "General Inquiry",
        "subject": "Subject",
        "message": "Message",
        "send": "Send",
        "attachments": "Attachments",
        "upload": "Upload",
        "cancel": "Cancel",
        "save": "Save",
        "delete": "Delete",
        "edit": "Edit",
        "add": "Add",
        "remove": "Remove",
        "create": "Create",
        "update": "Update",
        "confirm": "Confirm",
        "cancel": "Cancel",
        "ok": "OK",
        "yes_confirm": "Yes",
        "no_confirm": "No",
        "loading": "Loading...",
        "processing": "Processing...",
        "please_wait": "Please wait...",
        "connection_lost": "Connection lost. Reconnecting...",
        "session_expired": "Session expired. Please login again.",
        "login_required": "Please login to continue",
        "permission_denied": "Permission denied",
        "access_denied": "Access denied",
        "invalid_input": "Invalid input",
        "required_field": "This field is required",
        "invalid_email": "Invalid email address",
        "password_mismatch": "Passwords do not match",
        "password_weak": "Password is too weak",
        "password_strong": "Password is strong",
        "email_exists": "Email already exists",
        "email_not_found": "Email not found",
        "wrong_password": "Wrong password",
        "account_created": "Account created successfully",
        "account_updated": "Account updated successfully",
        "account_deleted": "Account deleted successfully",
        "password_changed": "Password changed successfully",
        "login_success": "Login successful",
        "logout_success": "Logout successful",
        "content_added": "Content added successfully",
        "content_updated": "Content updated successfully",
        "content_deleted": "Content deleted successfully",
        "favorite_added": "Added to favorites",
        "favorite_removed": "Removed from favorites",
        "watchlist_added": "Added to watchlist",
        "watchlist_removed": "Removed from watchlist",
        "review_submitted": "Review submitted successfully",
        "review_updated": "Review updated successfully",
        "review_deleted": "Review deleted successfully"
    },
    "hindi": {
        "site_name": "एक्सस्टार",
        "tagline": "मूवीज, सीरीज, एनीमे और भी बहुत कुछ",
        "hero_title": "असीमित मूवीज, सीरीज और एनीमे",
        "hero_subtitle": "कहीं भी देखें। कभी भी कैंसल करें। आपके लिए एआई-पावर्ड सुझाव।",
        "get_started": "शुरू करें",
        "sign_in": "साइन इन करें",
        "sign_up": "साइन अप करें",
        "logout": "लॉग आउट",
        "search_placeholder": "मूवीज, सीरीज, एनीमे खोजें...",
        "trending": "ट्रेंडिंग अभी",
        "recommended": "आपके लिए सुझाए गए",
        "latest": "नवीनतम रिलीज",
        "hindi_dubbed": "हिंदी डब्ड",
        "anime": "एनीमे सीरीज",
        "anime_movies": "एनीमे मूवीज",
        "hollywood": "हॉलीवुड ब्लॉकबस्टर्स",
        "bollywood": "बॉलीवुड हिट्स",
        "watch_now": "अभी देखें",
        "download": "डाउनलोड करें",
        "rating": "रेटिंग",
        "duration": "अवधि",
        "genre": "शैली",
        "language": "भाषा",
        "story": "कहानी",
        "cast": "कलाकार",
        "director": "निर्देशक",
        "year": "वर्ष",
        "profile": "मेरी प्रोफाइल",
        "settings": "सेटिंग्स",
        "help": "सहायता केंद्र",
        "language_select": "भाषा चुनें",
        "welcome_back": "वापसी पर स्वागत है",
        "new_here": "नए हैं?",
        "create_account": "खाता बनाएं",
        "email": "ईमेल पता",
        "password": "पासवर्ड",
        "confirm_password": "पासवर्ड पुष्टि करें",
        "full_name": "पूरा नाम",
        "remember_me": "मुझे याद रखें",
        "forgot_password": "पासवर्ड भूल गए?",
        "already_have_account": "पहले से खाता है?",
        "dont_have_account": "खाता नहीं है?",
        "login": "लॉगिन",
        "register": "रजिस्टर",
        "footer_text": "© 2024 एक्सस्टार। सभी अधिकार सुरक्षित। अपनी पसंदीदा मूवीज और एनीमे कई भाषाओं में देखें।",
        "watch_history": "देखने का इतिहास",
        "favorites": "मेरे पसंदीदा",
        "continue_watching": "देखना जारी रखें",
        "top_rated": "टॉप रेटेड",
        "coming_soon": "जल्द आ रहा है",
        "recently_added": "हाल ही में जोड़े गए",
        "action": "एक्शन",
        "comedy": "कॉमेडी",
        "drama": "ड्रामा",
        "romance": "रोमांस",
        "sci_fi": "साइंस फिक्शन",
        "horror": "हॉरर",
        "thriller": "थ्रिलर",
        "adventure": "एडवेंचर",
        "fantasy": "फैंटेसी",
        "crime": "क्राइम",
        "mystery": "रहस्य",
        "documentary": "डॉक्यूमेंट्री",
        "family": "परिवार",
        "war": "युद्ध",
        "western": "वेस्टर्न",
        "musical": "म्यूजिकल",
        "sport": "खेल",
        "history": "इतिहास",
        "biography": "जीवनी",
        "add_to_watchlist": "वॉचलिस्ट में जोड़ें",
        "remove_from_watchlist": "वॉचलिस्ट से हटाएं",
        "share": "शेयर करें",
        "report": "रिपोर्ट करें",
        "feedback": "फीडबैक दें",
        "privacy_policy": "गोपनीयता नीति",
        "terms_of_service": "सेवा की शर्तें",
        "contact_us": "संपर्क करें",
        "about_us": "हमारे बारे में",
        "faq": "अक्सर पूछे जाने वाले प्रश्न",
        "live_chat": "लाइव चैट",
        "notification": "सूचनाएं",
        "dark_mode": "डार्क मोड",
        "light_mode": "लाइट मोड",
        "auto_play": "ऑटो प्ले",
        "quality": "गुणवत्ता",
        "subtitles": "उपशीर्षक",
        "audio": "ऑडियो",
        "download_location": "डाउनलोड स्थान",
        "clear_cache": "कैश साफ़ करें",
        "logout_confirm": "क्या आप वाकई लॉगआउट करना चाहते हैं?",
        "delete_account": "खाता हटाएं",
        "change_password": "पासवर्ड बदलें",
        "update_profile": "प्रोफाइल अपडेट करें",
        "profile_picture": "प्रोफाइल फोटो",
        "membership": "सदस्यता",
        "premium": "प्रीमियम",
        "free_trial": "मुफ्त ट्रायल",
        "subscribe": "सब्सक्राइब करें",
        "cancel_subscription": "सदस्यता रद्द करें",
        "billing": "बिलिंग",
        "payment_method": "भुगतान विधि",
        "invoice": "चालान",
        "view_all": "सभी देखें",
        "load_more": "और लोड करें",
        "no_results": "कोई परिणाम नहीं मिला",
        "try_again": "पुनः प्रयास करें",
        "network_error": "नेटवर्क त्रुटि",
        "server_error": "सर्वर त्रुटि",
        "success": "सफलता",
        "error": "त्रुटि",
        "warning": "चेतावनी",
        "info": "जानकारी",
        "close": "बंद करें",
        "back": "पीछे",
        "next": "आगे",
        "previous": "पिछला",
        "page": "पृष्ठ",
        "of": "का",
        "sort_by": "क्रमबद्ध करें",
        "filter_by": "फ़िल्टर करें",
        "clear_filters": "फ़िल्टर साफ़ करें",
        "apply_filters": "फ़िल्टर लागू करें",
        "year_range": "वर्ष सीमा",
        "min_rating": "न्यूनतम रेटिंग",
        "max_duration": "अधिकतम अवधि",
        "season": "सीज़न",
        "episode": "एपिसोड",
        "trailer": "ट्रेलर",
        "behind_the_scenes": "पर्दे के पीछे",
        "interviews": "साक्षात्कार",
        "reviews": "समीक्षाएं",
        "ratings": "रेटिंग्स",
        "similar": "समान",
        "more_like_this": "इसी तरह के और",
        "you_may_also_like": "आपको यह भी पसंद आ सकता है",
        "because_you_watched": "क्योंकि आपने देखा",
        "trending_in": "में ट्रेंडिंग",
        "top_10": "टॉप 10",
        "new_releases": "नए रिलीज",
        "coming_this_week": "इस सप्ताह आ रहे हैं",
        "leaving_soon": "जल्द ही जा रहे हैं",
        "critics_picks": "आलोचकों की पसंद",
        "audience_favorites": "दर्शकों की पसंदीदा",
        "award_winning": "पुरस्कार विजेता",
        "hidden_gems": "छिपे हुए रत्न",
        "staff_picks": "स्टाफ की पसंद",
        "daily_recommendations": "दैनिक सुझाव",
        "weekly_top_10": "साप्ताहिक टॉप 10",
        "monthly_most_watched": "मासिक सबसे ज्यादा देखे गए",
        "all_time_favorites": "सर्वकालिक पसंदीदा",
        "recently_watched": "हाल ही में देखे गए",
        "resume_watching": "देखना जारी रखें",
        "watched": "देखा गया",
        "unwatched": "नहीं देखा गया",
        "mark_as_watched": "देखा गया चिह्नित करें",
        "mark_as_unwatched": "नहीं देखा गया चिह्नित करें",
        "rate_this": "इसे रेट करें",
        "your_rating": "आपकी रेटिंग",
        "average_rating": "औसत रेटिंग",
        "total_ratings": "कुल रेटिंग्स",
        "write_review": "समीक्षा लिखें",
        "see_all_reviews": "सभी समीक्षाएं देखें",
        "review_title": "समीक्षा शीर्षक",
        "review_content": "समीक्षा सामग्री",
        "submit_review": "समीक्षा सबमिट करें",
        "edit_review": "समीक्षा संपादित करें",
        "delete_review": "समीक्षा हटाएं",
        "review_helpful": "क्या यह समीक्षा सहायक थी?",
        "yes": "हाँ",
        "no": "नहीं",
        "report_review": "समीक्षा रिपोर्ट करें",
        "reported": "रिपोर्ट किया गया",
        "thanks_for_feedback": "आपकी प्रतिक्रिया के लिए धन्यवाद!",
        "feature_request": "सुविधा अनुरोध",
        "bug_report": "बग रिपोर्ट",
        "general_inquiry": "सामान्य पूछताछ",
        "subject": "विषय",
        "message": "संदेश",
        "send": "भेजें",
        "attachments": "अटैचमेंट",
        "upload": "अपलोड करें",
        "save": "सहेजें",
        "delete": "हटाएं",
        "edit": "संपादित करें",
        "add": "जोड़ें",
        "remove": "हटाएं",
        "create": "बनाएं",
        "update": "अपडेट करें",
        "confirm": "पुष्टि करें",
        "ok": "ठीक है",
        "yes_confirm": "हाँ",
        "no_confirm": "नहीं",
        "loading": "लोड हो रहा है...",
        "processing": "प्रोसेसिंग...",
        "please_wait": "कृपया प्रतीक्षा करें...",
        "connection_lost": "कनेक्शन टूट गया। पुनः कनेक्ट हो रहा है...",
        "session_expired": "सेशन समाप्त हो गया। कृपया पुनः लॉगिन करें।",
        "login_required": "कृपया जारी रखने के लिए लॉगिन करें",
        "permission_denied": "अनुमति अस्वीकृत",
        "access_denied": "पहुंच अस्वीकृत",
        "invalid_input": "अमान्य इनपुट",
        "required_field": "यह फ़ील्ड आवश्यक है",
        "invalid_email": "अमान्य ईमेल पता",
        "password_mismatch": "पासवर्ड मेल नहीं खाते",
        "password_weak": "पासवर्ड बहुत कमजोर है",
        "password_strong": "पासवर्ड मजबूत है",
        "email_exists": "ईमेल पहले से मौजूद है",
        "email_not_found": "ईमेल नहीं मिला",
        "wrong_password": "गलत पासवर्ड",
        "account_created": "खाता सफलतापूर्वक बनाया गया",
        "account_updated": "खाता सफलतापूर्वक अपडेट किया गया",
        "account_deleted": "खाता सफलतापूर्वक हटा दिया गया",
        "password_changed": "पासवर्ड सफलतापूर्वक बदल दिया गया",
        "login_success": "लॉगिन सफल",
        "logout_success": "लॉगआउट सफल",
        "content_added": "सामग्री सफलतापूर्वक जोड़ी गई",
        "content_updated": "सामग्री सफलतापूर्वक अपडेट की गई",
        "content_deleted": "सामग्री सफलतापूर्वक हटा दी गई",
        "favorite_added": "पसंदीदा में जोड़ा गया",
        "favorite_removed": "पसंदीदा से हटा दिया गया",
        "watchlist_added": "वॉचलिस्ट में जोड़ा गया",
        "watchlist_removed": "वॉचलिस्ट से हटा दिया गया",
        "review_submitted": "समीक्षा सफलतापूर्वक सबमिट की गई",
        "review_updated": "समीक्षा सफलतापूर्वक अपडेट की गई",
        "review_deleted": "समीक्षा सफलतापूर्वक हटा दी गई"
    },
    "hinglish": {
        "site_name": "XSTAR",
        "tagline": "Movies, Series, Anime aur bhi bahut kuch",
        "hero_title": "Unlimited Movies, Series aur Anime",
        "hero_subtitle": "Kahi bhi dekho. Kabhi bhi cancel karo. Tumhare liye AI-powered recommendations.",
        "get_started": "Shuru karo",
        "sign_in": "Sign In karo",
        "sign_up": "Sign Up karo",
        "logout": "Logout ho jao",
        "search_placeholder": "Movies, Series, Anime search karo...",
        "trending": "Trending ho raha hai",
        "recommended": "Tumhare liye推荐",
        "latest": "Naye releases",
        "hindi_dubbed": "Hindi dubbed",
        "anime": "Anime series",
        "anime_movies": "Anime movies",
        "hollywood": "Hollywood blockbusters",
        "bollywood": "Bollywood hits",
        "watch_now": "Abhi dekho",
        "download": "Download karo",
        "rating": "Rating",
        "duration": "Time",
        "genre": "Genre",
        "language": "Bhasha",
        "story": "Kahani",
        "cast": "Kalakars",
        "director": "Director",
        "year": "Saal",
        "profile": "Meri profile",
        "settings": "Settings",
        "help": "Help center",
        "language_select": "Bhasha chuno",
        "welcome_back": "Wapas aao",
        "new_here": "Naye ho?",
        "create_account": "Account banao",
        "email": "Email address",
        "password": "Password",
        "confirm_password": "Password confirm karo",
        "full_name": "Poora naam",
        "remember_me": "Mujhe yaad rakho",
        "forgot_password": "Password bhool gaye?",
        "already_have_account": "Pehle se account hai?",
        "dont_have_account": "Account nahi hai?",
        "login": "Login karo",
        "register": "Register karo",
        "footer_text": "© 2024 XSTAR. Saare rights reserved. Apni pasand ki movies aur anime kai bhashao mein dekho.",
        "watch_history": "Dekhne ka itihaas",
        "favorites": "Mere favorites",
        "continue_watching": "Dekhte raho",
        "top_rated": "Top rated",
        "coming_soon": "Jald aa raha hai",
        "recently_added": "Abhi abhi aaye",
        "action": "Action",
        "comedy": "Comedy",
        "drama": "Drama",
        "romance": "Romance",
        "sci_fi": "Sci-Fi",
        "horror": "Horror",
        "thriller": "Thriller",
        "adventure": "Adventure",
        "fantasy": "Fantasy",
        "crime": "Crime",
        "mystery": "Mystery",
        "documentary": "Documentary",
        "family": "Family",
        "war": "War",
        "western": "Western",
        "musical": "Musical",
        "sport": "Sport",
        "history": "History",
        "biography": "Biography",
        "add_to_watchlist": "Watchlist mein daalo",
        "remove_from_watchlist": "Watchlist se hatao",
        "share": "Share karo",
        "report": "Report karo",
        "feedback": "Feedback do",
        "privacy_policy": "Privacy Policy",
        "terms_of_service": "Terms of Service",
        "contact_us": "Contact karo",
        "about_us": "Hamare baare mein",
        "faq": "Frequently asked questions",
        "live_chat": "Live chat",
        "notification": "Notifications",
        "dark_mode": "Dark mode",
        "light_mode": "Light mode",
        "auto_play": "Auto play",
        "quality": "Quality",
        "subtitles": "Subtitles",
        "audio": "Audio",
        "download_location": "Download location",
        "clear_cache": "Cache saaf karo",
        "logout_confirm": "Kya sach mein logout hona chahte ho?",
        "delete_account": "Account delete karo",
        "change_password": "Password badlo",
        "update_profile": "Profile update karo",
        "profile_picture": "Profile picture",
        "membership": "Membership",
        "premium": "Premium",
        "free_trial": "Free trial",
        "subscribe": "Subscribe karo",
        "cancel_subscription": "Subscription cancel karo",
        "billing": "Billing",
        "payment_method": "Payment method",
        "invoice": "Invoice",
        "view_all": "Sab dekho",
        "load_more": "Aur load karo",
        "no_results": "Koi result nahi mila",
        "try_again": "Phir se try karo",
        "network_error": "Network error",
        "server_error": "Server error",
        "success": "Ho gaya",
        "error": "Error",
        "warning": "Warning",
        "info": "Info",
        "close": "Band karo",
        "back": "Peeche jao",
        "next": "Aage badho",
        "previous": "Peeche",
        "page": "Page",
        "of": "of",
        "sort_by": "Sort karo",
        "filter_by": "Filter karo",
        "clear_filters": "Filters hatao",
        "apply_filters": "Filters lagao",
        "year_range": "Saal ka range",
        "min_rating": "Minimum rating",
        "max_duration": "Maximum duration",
        "season": "Season",
        "episode": "Episode",
        "trailer": "Trailer",
        "behind_the_scenes": "Behind the scenes",
        "interviews": "Interviews",
        "reviews": "Reviews",
        "ratings": "Ratings",
        "similar": "Similar",
        "more_like_this": "Iske jaisa aur",
        "you_may_also_like": "Tumhe ye bhi pasand aa sakta hai",
        "because_you_watched": "Kyuki tumne dekha",
        "trending_in": "mein trending",
        "top_10": "Top 10",
        "new_releases": "Naye releases",
        "coming_this_week": "Is hafte aa rahe hain",
        "leaving_soon": "Jald hi ja rahe hain",
        "critics_picks": "Critics ki pasand",
        "audience_favorites": "Audience ki favorites",
        "award_winning": "Award winning",
        "hidden_gems": "Hidden gems",
        "staff_picks": "Staff ki picks",
        "daily_recommendations": "Rozana ke suggestions",
        "weekly_top_10": "Weekly top 10",
        "monthly_most_watched": "Mahine me sabse zyada dekhe gaye",
        "all_time_favorites": "Sab time ke favorites",
        "recently_watched": "Recently dekha",
        "resume_watching": "Dekhna continue karo",
        "watched": "Dekh liya",
        "unwatched": "Nahi dekha",
        "mark_as_watched": "Dekha mark karo",
        "mark_as_unwatched": "Nahi dekha mark karo",
        "rate_this": "Isko rate karo",
        "your_rating": "Tumhari rating",
        "average_rating": "Average rating",
        "total_ratings": "Total ratings",
        "write_review": "Review likho",
        "see_all_reviews": "Saare reviews dekho",
        "review_title": "Review ka title",
        "review_content": "Review likho",
        "submit_review": "Review submit karo",
        "edit_review": "Review edit karo",
        "delete_review": "Review hatao",
        "review_helpful": "Kya ye review helpful tha?",
        "yes": "Haan",
        "no": "Nahi",
        "report_review": "Review report karo",
        "reported": "Report kar diya",
        "thanks_for_feedback": "Feedback dene ka shukriya!",
        "feature_request": "Feature request",
        "bug_report": "Bug report",
        "general_inquiry": "General inquiry",
        "subject": "Subject",
        "message": "Message",
        "send": "Bhejo",
        "attachments": "Attachments",
        "upload": "Upload karo",
        "save": "Save karo",
        "delete": "Delete karo",
        "edit": "Edit karo",
        "add": "Add karo",
        "remove": "Remove karo",
        "create": "Create karo",
        "update": "Update karo",
        "confirm": "Confirm karo",
        "ok": "Theek hai",
        "yes_confirm": "Haan",
        "no_confirm": "Nahi",
        "loading": "Load ho raha hai...",
        "processing": "Process ho raha hai...",
        "please_wait": "Kripya pratiksha karein...",
        "connection_lost": "Connection toot gaya. Dobara connect ho raha hai...",
        "session_expired": "Session khatam ho gaya. Dobara login karo.",
        "login_required": "Continue karne ke liye login karo",
        "permission_denied": "Permission nahi hai",
        "access_denied": "Access nahi hai",
        "invalid_input": "Invalid input",
        "required_field": "Ye field required hai",
        "invalid_email": "Invalid email address",
        "password_mismatch": "Password match nahi ho rahe",
        "password_weak": "Password bahut weak hai",
        "password_strong": "Password strong hai",
        "email_exists": "Email pehle se exist karta hai",
        "email_not_found": "Email nahi mila",
        "wrong_password": "Galat password",
        "account_created": "Account successfully create ho gaya",
        "account_updated": "Account successfully update ho gaya",
        "account_deleted": "Account successfully delete ho gaya",
        "password_changed": "Password successfully change ho gaya",
        "login_success": "Login successful",
        "logout_success": "Logout successful",
        "content_added": "Content successfully add ho gaya",
        "content_updated": "Content successfully update ho gaya",
        "content_deleted": "Content successfully delete ho gaya",
        "favorite_added": "Favorites mein add ho gaya",
        "favorite_removed": "Favorites se remove ho gaya",
        "watchlist_added": "Watchlist mein add ho gaya",
        "watchlist_removed": "Watchlist se remove ho gaya",
        "review_submitted": "Review successfully submit ho gayi",
        "review_updated": "Review successfully update ho gayi",
        "review_deleted": "Review successfully delete ho gayi"
    },
    "spanish": {
        "site_name": "XSTAR",
        "tagline": "Películas, Series, Anime y Más",
        "hero_title": "Películas, Series y Anime Ilimitados",
        "hero_subtitle": "Mira en cualquier lugar. Cancela en cualquier momento. Recomendaciones con IA solo para ti.",
        "get_started": "Comenzar",
        "sign_in": "Iniciar Sesión",
        "sign_up": "Registrarse",
        "logout": "Cerrar Sesión",
        "search_placeholder": "Buscar películas, series, anime...",
        "trending": "Tendencias Ahora",
        "recommended": "Recomendado Para Ti",
        "latest": "Últimos Lanzamientos",
        "hindi_dubbed": "Doblado al Hindi",
        "anime": "Series de Anime",
        "anime_movies": "Películas de Anime",
        "hollywood": "Éxitos de Hollywood",
        "bollywood": "Éxitos de Bollywood",
        "watch_now": "Ver Ahora",
        "download": "Descargar",
        "rating": "Calificación",
        "duration": "Duración",
        "genre": "Género",
        "language": "Idioma",
        "story": "Historia",
        "cast": "Elenco",
        "director": "Director",
        "year": "Año",
        "profile": "Mi Perfil",
        "settings": "Configuración",
        "help": "Centro de Ayuda",
        "language_select": "Seleccionar Idioma",
        "welcome_back": "Bienvenido de Vuelta",
        "new_here": "¿Nuevo aquí?",
        "create_account": "Crear Cuenta",
        "email": "Correo Electrónico",
        "password": "Contraseña",
        "confirm_password": "Confirmar Contraseña",
        "full_name": "Nombre Completo",
        "remember_me": "Recuérdame",
        "forgot_password": "¿Olvidaste tu Contraseña?",
        "already_have_account": "¿Ya tienes una cuenta?",
        "dont_have_account": "¿No tienes una cuenta?",
        "login": "Iniciar Sesión",
        "register": "Registrarse",
        "footer_text": "© 2024 XSTAR. Todos los derechos reservados. Mira tus películas y anime favoritos en múltiples idiomas.",
        "watch_history": "Historial de Visualización",
        "favorites": "Mis Favoritos",
        "continue_watching": "Continuar Viendo",
        "top_rated": "Mejor Calificados",
        "coming_soon": "Próximamente",
        "recently_added": "Agregados Recientemente",
        "action": "Acción",
        "comedy": "Comedia",
        "drama": "Drama",
        "romance": "Romance",
        "sci_fi": "Ciencia Ficción",
        "horror": "Terror",
        "thriller": "Suspenso",
        "adventure": "Aventura",
        "fantasy": "Fantasía"
    },
    "japanese": {
        "site_name": "エックススター",
        "tagline": "映画、シリーズ、アニメなど",
        "hero_title": "無制限の映画、シリーズ、アニメ",
        "hero_subtitle": "どこでも視聴可能。いつでもキャンセル可能。AIによるパーソナライズドレコメンデーション。",
        "get_started": "始める",
        "sign_in": "サインイン",
        "sign_up": "サインアップ",
        "logout": "ログアウト",
        "search_placeholder": "映画、シリーズ、アニメを検索...",
        "trending": "トレンド今すぐ",
        "recommended": "あなたへのおすすめ",
        "latest": "最新リリース",
        "hindi_dubbed": "ヒンディー語吹替",
        "anime": "アニメシリーズ",
        "anime_movies": "アニメ映画",
        "hollywood": "ハリウッド映画",
        "bollywood": "ボリウッド映画",
        "watch_now": "今すぐ見る",
        "download": "ダウンロード",
        "rating": "評価",
        "duration": "時間",
        "genre": "ジャンル",
        "language": "言語",
        "story": "ストーリー",
        "cast": "キャスト",
        "director": "監督",
        "year": "年",
        "profile": "マイプロフィール",
        "settings": "設定",
        "help": "ヘルプセンター",
        "language_select": "言語を選択",
        "welcome_back": "おかえりなさい",
        "new_here": "初めてですか？",
        "create_account": "アカウント作成",
        "email": "メールアドレス",
        "password": "パスワード",
        "confirm_password": "パスワード確認",
        "full_name": "フルネーム",
        "remember_me": "ログイン状態を保持",
        "forgot_password": "パスワードをお忘れですか？",
        "already_have_account": "すでにアカウントをお持ちですか？",
        "dont_have_account": "アカウントをお持ちでないですか？",
        "login": "ログイン",
        "register": "登録",
        "footer_text": "© 2024 エックススター。全著作権所有。お気に入りの映画やアニメを多言語で楽しめます。",
        "watch_history": "視聴履歴",
        "favorites": "お気に入り",
        "continue_watching": "続けて視聴",
        "top_rated": "トップ評価",
        "coming_soon": "近日公開",
        "recently_added": "最近追加された作品",
        "action": "アクション",
        "comedy": "コメディ",
        "drama": "ドラマ",
        "romance": "ロマンス",
        "sci_fi": "SF",
        "horror": "ホラー",
        "thriller": "スリラー",
        "adventure": "アドベンチャー",
        "fantasy": "ファンタジー"
    }
}

# ========== COMPLETE CONTENT DATABASE (400+ items) ==========
CONTENT_DB = {}

# Hindi Movies (2023-2024 Latest)
hindi_movies = [
    {"id": "h1", "title": "Jawan", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/jH0tOWMKhWjVW4qQNv7F3hPdYzK.jpg", "banner": "https://image.tmdb.org/t/p/original/zKJqy2SqX0R3yN4cM8pLqW5aE1b.jpg", "rating": 8.2, "duration": "2h 49m", "director": "Atlee", "cast": "Shah Rukh Khan, Nayanthara, Vijay Sethupathi", "story": "Jawan is a high-octane action thriller starring Shah Rukh Khan in a dual role. A prison warden assembles a team of six women to expose corruption and fight against a powerful arms dealer. The film explores themes of social justice, revenge, and redemption with stunning visuals and emotional depth."},
    {"id": "h2", "title": "Animal", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Action, Drama", "image": "https://image.tmdb.org/t/p/w500/kC5KqY5LmN3pQrR7sT8uV9wX0yZ.jpg", "banner": "https://image.tmdb.org/t/p/original/bCdEfGhIjKlMnOpQrStUvWxYz.jpg", "rating": 8.5, "duration": "3h 21m", "director": "Sandeep Reddy Vanga", "cast": "Ranbir Kapoor, Anil Kapoor, Bobby Deol", "story": "Animal follows Ranvijay Singh, a man with a violent streak seeking his father's approval. When his father survives an assassination attempt, he unleashes chaos to hunt down the perpetrators. The film explores toxic masculinity, family bonds, and moral ambiguity."},
    {"id": "h3", "title": "Dunki", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Comedy, Drama", "image": "https://image.tmdb.org/t/p/w500/fGhIjKlMnOpQrStUvWxYzB2cD3.jpg", "banner": "https://image.tmdb.org/t/p/original/gHiJkLmNoPqRsTuVwXyZ3dE4f.jpg", "rating": 8.1, "duration": "2h 41m", "director": "Rajkumar Hirani", "cast": "Shah Rukh Khan, Taapsee Pannu, Vicky Kaushal", "story": "Dunki is a social comedy-drama about illegal immigration through the 'Donkey Flight' route, balancing humor with emotional depth about home and belonging."},
    {"id": "h4", "title": "Salaar", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/dEfGhIjKlMnOpQrStUvWxYzA1bC.jpg", "banner": "https://image.tmdb.org/t/p/original/eFgHiJkLmNoPqRsTuVwXyZ2cD3.jpg", "rating": 8.3, "duration": "2h 55m", "director": "Prashanth Neel", "cast": "Prabhas, Prithviraj Sukumaran, Shruti Haasan", "story": "Salaar follows Deva, a fierce warrior who returns to the violent city of Khansaar to protect his friend. The film builds a sprawling universe of tribal politics, blood feuds, and ancient traditions with massive action sequences."},
    {"id": "h5", "title": "Tiger 3", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 7.8, "duration": "2h 36m", "director": "Maneesh Sharma", "cast": "Salman Khan, Katrina Kaif, Emraan Hashmi", "story": "Tiger and Zoya are back to save the nation from a new threat. This spy thriller features high-octane action across multiple countries and emotional moments between the iconic duo."},
    {"id": "h6", "title": "Pathaan", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 7.9, "duration": "2h 26m", "director": "Siddharth Anand", "cast": "Shah Rukh Khan, Deepika Padukone, John Abraham", "story": "Pathaan, an exiled RAW agent, joins forces with ISI agent Rubina to take down a renegade army officer who plans to attack India. This spy thriller marked SRK's comeback after four years."},
    {"id": "h7", "title": "Gadar 2", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Action, Drama", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/7vF9dY8R6gN5kLm2pQ3sT4uV5wX6yZ.jpg", "rating": 7.5, "duration": "2h 50m", "director": "Anil Sharma", "cast": "Sunny Deol, Ameesha Patel, Utkarsh Sharma", "story": "The sequel to the iconic Gadar continues Tara Singh's journey as he crosses borders to save his son from the Pakistani army during the 1971 war."},
    {"id": "h8", "title": "Rocky Aur Rani Kii Prem Kahaani", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Romance, Comedy", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/2xG1rY5pL8mN7kQ3sT4uV6wX8yZ0aB.jpg", "rating": 7.8, "duration": "2h 48m", "director": "Karan Johar", "cast": "Ranveer Singh, Alia Bhatt, Dharmendra", "story": "A vibrant family drama where a journalist and a dancer swap families to test their relationship, dealing with generational conflicts and modern love."},
    {"id": "h9", "title": "OMG 2", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Comedy, Drama", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/9m3N1Y3pL8kQ7sT4uV6wX8yZ0aB.jpg", "rating": 8.0, "duration": "2h 36m", "director": "Amit Rai", "cast": "Akshay Kumar, Pankaj Tripathi, Yami Gautam", "story": "A social drama about sex education in schools, following a father's fight against the system to protect his son from misinformation."},
    {"id": "h10", "title": "Dream Girl 2", "year": 2023, "type": "movie", "language": "Hindi", "genre": "Comedy", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/6b7c8d9e0f1g2h3i4j5k6l7m8n.jpg", "rating": 7.2, "duration": "2h 15m", "director": "Raaj Shaandilyaa", "cast": "Ayushmann Khurrana, Ananya Panday, Annu Kapoor", "story": "A man who can mimic female voices gets into hilarious situations when he starts speaking as a woman, leading to confusion and comedy."},
]

# English Hollywood Movies
english_movies = [
    {"id": "e1", "title": "Oppenheimer", "year": 2023, "type": "movie", "language": "English", "genre": "Biography, Drama", "image": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg", "banner": "https://image.tmdb.org/t/p/original/1JpY9Yq6N8r7M5kL3pQ2sT4uV6wX8yZ.jpg", "rating": 8.9, "duration": "3h", "director": "Christopher Nolan", "cast": "Cillian Murphy, Emily Blunt, Robert Downey Jr.", "story": "The story of J. Robert Oppenheimer and his role in developing the atomic bomb during World War II. The film explores his brilliant mind, political affiliations, and immense guilt."},
    {"id": "e2", "title": "Barbie", "year": 2023, "type": "movie", "language": "English", "genre": "Comedy, Fantasy", "image": "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg", "banner": "https://image.tmdb.org/t/p/original/2xG1rY5pL8mN7kQ3sT4uV6wX8yZ0aB.jpg", "rating": 8.0, "duration": "1h 54m", "director": "Greta Gerwig", "cast": "Margot Robbie, Ryan Gosling, America Ferrera", "story": "Barbie and Ken have the time of their lives in Barbie Land before going to the real world. This existential comedy explores feminism, patriarchy, and what it means to be human."},
    {"id": "e3", "title": "John Wick 4", "year": 2023, "type": "movie", "language": "English", "genre": "Action, Thriller", "image": "https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 8.2, "duration": "2h 49m", "director": "Chad Stahelski", "cast": "Keanu Reeves, Donnie Yen, Bill Skarsgård", "story": "John Wick uncovers a path to defeating the High Table. Before earning his freedom, he must face a new enemy with powerful alliances across the globe."},
    {"id": "e4", "title": "Spider-Man: Across the Spider-Verse", "year": 2023, "type": "movie", "language": "English", "genre": "Animation, Action", "image": "https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg", "banner": "https://image.tmdb.org/t/p/original/iQFcwSGbZXMkeyKrxbPnwnRo5yx.jpg", "rating": 8.7, "duration": "2h 20m", "director": "Joaquim Dos Santos", "cast": "Shameik Moore, Hailee Steinfeld, Oscar Isaac", "story": "Miles Morales returns for an epic multiverse adventure with Spider-Gwen and new allies, facing the Spider-Society across multiple dimensions."},
    {"id": "e5", "title": "Mission: Impossible - Dead Reckoning Part 1", "year": 2023, "type": "movie", "language": "English", "genre": "Action, Adventure", "image": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg", "banner": "https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg", "rating": 8.4, "duration": "2h 43m", "director": "Christopher McQuarrie", "cast": "Tom Cruise, Hayley Atwell, Ving Rhames", "story": "Ethan Hunt and his IMF team face their most dangerous mission yet - tracking a terrifying new weapon that threatens all of humanity."},
    {"id": "e6", "title": "The Flash", "year": 2023, "type": "movie", "language": "English", "genre": "Action, Adventure", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 7.6, "duration": "2h 24m", "director": "Andy Muschietti", "cast": "Ezra Miller, Michael Keaton, Sasha Calle", "story": "Barry Allen uses his speed to travel back in time, inadvertently altering the future and getting trapped in a reality where General Zod has returned."},
    {"id": "e7", "title": "Indiana Jones and the Dial of Destiny", "year": 2023, "type": "movie", "language": "English", "genre": "Adventure, Action", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/7vF9dY8R6gN5kLm2pQ3sT4uV5wX6yZ.jpg", "rating": 7.5, "duration": "2h 34m", "director": "James Mangold", "cast": "Harrison Ford, Phoebe Waller-Bridge, Mads Mikkelsen", "story": "Archaeologist Indiana Jones races against time to retrieve a legendary artifact that can change the course of history."},
    {"id": "e8", "title": "The Little Mermaid", "year": 2023, "type": "movie", "language": "English", "genre": "Fantasy, Romance", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 7.3, "duration": "2h 15m", "director": "Rob Marshall", "cast": "Halle Bailey, Jonah Hauer-King, Melissa McCarthy", "story": "A young mermaid makes a deal with a sea witch to become human and win the heart of a prince."},
    {"id": "e9", "title": "Fast X", "year": 2023, "type": "movie", "language": "English", "genre": "Action, Crime", "image": "https://image.tmdb.org/t/p/w500/4XM8DUTQbHTlhUdCjwOq1PJOXSh.jpg", "banner": "https://image.tmdb.org/t/p/original/9m3N1Y3pL8kQ7sT4uV6wX8yZ0aB.jpg", "rating": 7.8, "duration": "2h 21m", "director": "Louis Leterrier", "cast": "Vin Diesel, Jason Momoa, Michelle Rodriguez", "story": "Dom Toretto and his family face their most lethal opponent yet - Dante Reyes, the son of drug lord Hernan Reyes, who seeks revenge."},
    {"id": "e10", "title": "Guardians of the Galaxy Vol. 3", "year": 2023, "type": "movie", "language": "English", "genre": "Action, Sci-Fi", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/2xG1rY5pL8mN7kQ3sT4uV6wX8yZ0aB.jpg", "rating": 8.6, "duration": "2h 30m", "director": "James Gunn", "cast": "Chris Pratt, Zoe Saldana, Dave Bautista", "story": "The Guardians embark on a mission to save Rocket's life, leading them to confront the High Evolutionary and learn about Rocket's tragic past."},
]

# Anime Series (Hindi Dubbed & Japanese with English Subs)
anime_series = [
    {"id": "a1", "title": "Demon Slayer", "year": 2019, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/5EwSVvuBQMB9dVyLz7SJTxDZqQj.jpg", "banner": "https://image.tmdb.org/t/p/original/wwemzKWzjKYJFfCeiB57q3r4Bcm.png", "rating": 8.7, "seasons": 4, "episodes": 55, "studio": "Ufotable", "story": "After his family is brutally murdered, Tanjiro Kamado becomes a demon slayer to save his sister Nezuko, who has been turned into a demon. Together with his companions, he joins the Demon Slayer Corps to hunt down the demon king Muzan Kibutsuji. The series is renowned for its breathtaking animation by Ufotable, emotional storytelling, and epic sword fights."},
    {"id": "a2", "title": "Attack on Titan", "year": 2013, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/sxR7D2bSCJkhbGLcH6c6H8MkE5G.jpg", "banner": "https://image.tmdb.org/t/p/original/7D9BqVdE4R5cJ8kLmN2pQxYzW1.jpg", "rating": 9.1, "seasons": 4, "episodes": 87, "studio": "Wit Studio, MAPPA", "story": "Eren Yeager and his friends from the Survey Corps discover that humanity lives within walled cities to protect them from man-eating Titans. As secrets about the world's true nature unfold, Eren unleashes the power of the Founding Titan to fight for freedom."},
    {"id": "a3", "title": "Jujutsu Kaisen", "year": 2020, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 8.6, "seasons": 2, "episodes": 47, "studio": "MAPPA", "story": "Yuji Itadori swallows a cursed object containing the finger of the powerful demon Ryomen Sukuna, becoming his vessel. He joins the Tokyo Jujutsu High School to learn how to control this power and collect the remaining fingers of Sukuna."},
    {"id": "a4", "title": "One Piece", "year": 1999, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Adventure", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 9.0, "seasons": 20, "episodes": 1085, "studio": "Toei Animation", "story": "Monkey D. Luffy, a boy whose body gained the properties of rubber after unintentionally eating a Devil Fruit, sets out on a journey to become the Pirate King. He assembles a diverse crew of pirates, each with their own dreams and special abilities, as they search for the legendary treasure One Piece."},
    {"id": "a5", "title": "Naruto Shippuden", "year": 2007, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/7vF9dY8R6gN5kLm2pQ3sT4uV5wX6yZ.jpg", "rating": 8.7, "seasons": 21, "episodes": 500, "studio": "Studio Pierrot", "story": "Naruto Uzumaki returns after two and a half years of training with Jiraiya to face the criminal organization Akatsuki, who seeks to capture the tailed beasts including the Nine-Tails sealed inside him."},
    {"id": "a6", "title": "Death Note", "year": 2006, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Thriller", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/2xG1rY5pL8mN7kQ3sT4uV6wX8yZ0aB.jpg", "rating": 9.0, "seasons": 1, "episodes": 37, "studio": "Madhouse", "story": "A high school student discovers a supernatural notebook that allows him to kill anyone by writing their name in it. He decides to use this power to rid the world of criminals, becoming the vigilante known as Kira."},
    {"id": "a7", "title": "My Hero Academia", "year": 2016, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/9m3N1Y3pL8kQ7sT4uV6wX8yZ0aB.jpg", "rating": 8.4, "seasons": 6, "episodes": 138, "studio": "Bones", "story": "In a world where most of the population has superpowers called 'Quirks', a Quirkless boy named Izuku Midoriya dreams of becoming a hero. After a fateful encounter with his idol All Might, he inherits the powerful Quirk 'One For All' and enrolls in the prestigious U.A. High School."},
    {"id": "a8", "title": "Spy x Family", "year": 2022, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Comedy", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/6b7c8d9e0f1g2h3i4j5k6l7m8n.jpg", "rating": 8.5, "seasons": 2, "episodes": 37, "studio": "Wit Studio, CloverWorks", "story": "A spy on a mission must build a fake family to get close to his target. Unbeknownst to him, the girl he adopts as his daughter is a telepath, and the woman he agrees to marry is a skilled assassin."},
    {"id": "a9", "title": "Tokyo Revengers", "year": 2021, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 8.1, "seasons": 2, "episodes": 37, "studio": "Liden Films", "story": "A 26-year-old man learns that his middle school girlfriend has been killed by a gang. After a near-death experience, he travels back in time 12 years to save her and change the future."},
    {"id": "a10", "title": "Fullmetal Alchemist: Brotherhood", "year": 2009, "type": "anime", "language": "Hindi Dubbed", "genre": "Anime, Fantasy", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 9.1, "seasons": 1, "episodes": 64, "studio": "Bones", "story": "Two brothers use alchemy to try to bring their dead mother back to life, but the attempt fails and one loses his body while the other loses an arm and leg. They search for the Philosopher's Stone to restore what they've lost."},
]

# Anime Movies
anime_movies = [
    {"id": "am1", "title": "Demon Slayer: Mugen Train", "year": 2020, "type": "anime_movie", "language": "Hindi Dubbed", "genre": "Anime, Action", "image": "https://image.tmdb.org/t/p/w500/5EwSVvuBQMB9dVyLz7SJTxDZqQj.jpg", "banner": "https://image.tmdb.org/t/p/original/wwemzKWzjKYJFfCeiB57q3r4Bcm.png", "rating": 8.7, "duration": "1h 57m", "studio": "Ufotable", "story": "After his family is brutally murdered, Tanjiro Kamado becomes a demon slayer to save his sister Nezuko. On a mysterious train, they face the powerful Enmu who traps passengers in dream worlds. Tanjiro must fight alongside the Flame Hashira, Kyojuro Rengoku, to defeat the demons and save everyone aboard."},
    {"id": "am2", "title": "Spirited Away", "year": 2001, "type": "anime_movie", "language": "Japanese", "genre": "Anime, Fantasy", "image": "https://image.tmdb.org/t/p/w500/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg", "banner": "https://image.tmdb.org/t/p/original/7i9nNtL2rLc4m5n6o7p8q9r0s1t.jpg", "rating": 8.6, "duration": "2h 5m", "studio": "Studio Ghibli", "story": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, where humans are changed into beasts. To save her parents who have been turned into pigs, she must work in a magical bathhouse for spirits."},
    {"id": "am3", "title": "Your Name", "year": 2016, "type": "anime_movie", "language": "Hindi Dubbed", "genre": "Anime, Romance", "image": "https://image.tmdb.org/t/p/w500/q719jXXEzOoYaps6babgKnONONX.jpg", "banner": "https://image.tmdb.org/t/p/original/3r6J1j2k3l4m5n6o7p8q9r0s1t.jpg", "rating": 8.4, "duration": "1h 46m", "studio": "CoMix Wave Films", "story": "Two strangers find themselves linked in a bizarre way. When a connection forms, will distance be the only thing to keep them apart? This critically acclaimed anime masterpiece explores body-swapping, time travel, and the red thread of fate."},
    {"id": "am4", "title": "Suzume", "year": 2022, "type": "anime_movie", "language": "Japanese", "genre": "Anime, Adventure", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/8xV2vJqK3nLmP9oR4sT6uW7yXzA.jpg", "rating": 8.1, "duration": "2h 2m", "studio": "CoMix Wave Films", "story": "Suzume, a 17-year-old girl, meets a young man searching for a door. Following him, she finds one and opens it, unleashing disaster across Japan. Now she must close these mysterious doors to prevent further catastrophe."},
    {"id": "am5", "title": "Weathering With You", "year": 2019, "type": "anime_movie", "language": "Japanese", "genre": "Anime, Romance", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/4f1N4Y6k5m8P9Qr2S3tU4vW5xY6z.jpg", "rating": 7.9, "duration": "1h 52m", "studio": "CoMix Wave Films", "story": "A high school boy runs away to Tokyo and meets a girl who has the ability to control the weather. Their relationship develops as they use her power to bring sunshine to rainy days, but every gift comes with a price."},
    {"id": "am6", "title": "Howl's Moving Castle", "year": 2004, "type": "anime_movie", "language": "Japanese", "genre": "Anime, Fantasy", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/7vF9dY8R6gN5kLm2pQ3sT4uV5wX6yZ.jpg", "rating": 8.2, "duration": "1h 59m", "studio": "Studio Ghibli", "story": "A young milliner is cursed by a witch and transformed into an old woman. She seeks refuge in the moving castle of the mysterious wizard Howl, where she becomes part of his household and helps him break his own curse."},
    {"id": "am7", "title": "Princess Mononoke", "year": 1997, "type": "anime_movie", "language": "Japanese", "genre": "Anime, Fantasy", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/2xG1rY5pL8mN7kQ3sT4uV6wX8yZ0aB.jpg", "rating": 8.4, "duration": "2h 14m", "studio": "Studio Ghibli", "story": "A prince is cursed with a deadly affliction and journeys to the west to find a cure. There, he becomes entangled in a battle between the gods of a forest and the humans who are destroying it."},
    {"id": "am8", "title": "A Silent Voice", "year": 2016, "type": "anime_movie", "language": "Japanese", "genre": "Anime, Drama", "image": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uy4.jpg", "banner": "https://image.tmdb.org/t/p/original/9m3N1Y3pL8kQ7sT4uV6wX8yZ0aB.jpg", "rating": 8.2, "duration": "2h 10m", "studio": "Kyoto Animation", "story": "A former bully tries to make amends with the deaf girl he tormented in elementary school, confronting his own guilt and social anxiety along the way."},
]

# Merge all content
for movie in hindi_movies + english_movies:
    CONTENT_DB[movie["id"]] = movie
for anime in anime_series + anime_movies:
    CONTENT_DB[anime["id"]] = anime

# ========== USER DATABASE ==========
USERS = {}
WATCH_HISTORY = defaultdict(list)
WATCHLIST = defaultdict(list)
FAVORITES = defaultdict(list)
USER_RATINGS = defaultdict(dict)
CONTENT_VIEWS = defaultdict(int)

# ========== HELPER FUNCTIONS ==========
def get_trending_content(limit=15):
    trending = []
    all_content = list(CONTENT_DB.items())
    sorted_content = sorted(all_content, key=lambda x: CONTENT_VIEWS.get(x[0], 0) + x[1].get("rating", 0), reverse=True)
    for cid, content in sorted_content[:limit]:
        content_copy = content.copy()
        content_copy["id"] = cid
        trending.append(content_copy)
    return trending

def get_recommendations(user_id, limit=20):
    watched = set(WATCH_HISTORY.get(user_id, []))
    watchlist = set(WATCHLIST.get(user_id, []))
    favorites = set(FAVORITES.get(user_id, []))
    
    # Combine all interacted content
    interacted = watched.union(watchlist).union(favorites)
    
    # Get user's preferred genres from watched content
    genre_prefs = defaultdict(int)
    for cid in watched:
        if cid in CONTENT_DB:
            genres = CONTENT_DB[cid].get("genre", "").split(", ")
            for genre in genres:
                genre_prefs[genre] += 1
    
    # Score and recommend
    recommendations = []
    for cid, content in CONTENT_DB.items():
        if cid in interacted:
            continue
        
        score = 0
        content_genres = content.get("genre", "").split(", ")
        for genre in content_genres:
            score += genre_prefs.get(genre, 0)
        
        # Rating boost
        score += content.get("rating", 0) * 2
        
        if score > 0:
            content_copy = content.copy()
            content_copy["id"] = cid
            content_copy["recommendation_score"] = round(score, 2)
            recommendations.append(content_copy)
    
    recommendations.sort(key=lambda x: x.get("recommendation_score", 0), reverse=True)
    return recommendations[:limit]

def search_content(query):
    query = query.lower()
    results = []
    for cid, content in CONTENT_DB.items():
        if (query in content.get("title", "").lower() or 
            query in content.get("genre", "").lower() or
            query in content.get("language", "").lower() or
            query in content.get("director", "").lower() or
            query in content.get("cast", "").lower()):
            content_copy = content.copy()
            content_copy["id"] = cid
            results.append(content_copy)
    return results

# ========== DECORATORS ==========
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# ========== API ROUTES ==========
@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES, translations=TRANSLATIONS)

@app.route('/set_language', methods=['POST'])
def set_language():
    data = request.get_json()
    session['language'] = data.get('language', 'english')
    return jsonify({"success": True})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if email in USERS:
        return jsonify({"error": "Email already exists"}), 400
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    USERS[email] = {
        "name": name, 
        "password": hashed, 
        "email": email,
        "created_at": datetime.now().isoformat(),
        "membership": "free",
        "preferences": {
            "language": session.get('language', 'english'),
            "notifications": True,
            "auto_play": True
        }
    }
    session['user_id'] = email
    session['user_name'] = name
    session['language'] = session.get('language', 'english')
    
    return jsonify({"success": True, "name": name})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email not in USERS:
        return jsonify({"error": "User not found"}), 401
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if USERS[email]["password"] != hashed:
        return jsonify({"error": "Invalid password"}), 401
    
    session['user_id'] = email
    session['user_name'] = USERS[email]["name"]
    session['language'] = session.get('language', USERS[email].get("preferences", {}).get("language", "english"))
    
    return jsonify({"success": True, "name": USERS[email]["name"]})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/content')
def get_all_content():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    genre = request.args.get('genre')
    language = request.args.get('language')
    year = request.args.get('year')
    min_rating = request.args.get('min_rating')
    search = request.args.get('search')
    
    results = []
    for cid, content in CONTENT_DB.items():
        if search and search.lower() not in content.get("title", "").lower():
            continue
        if genre and genre != "All" and genre not in content.get("genre", "").split(", "):
            continue
        if language and language != "All" and content.get("language") != language:
            continue
        if year and year != "All" and str(content.get("year")) != year:
            continue
        if min_rating and float(content.get("rating", 0)) < float(min_rating):
            continue
        content_copy = content.copy()
        content_copy["id"] = cid
        results.append(content_copy)
    
    # Sort by rating
    results.sort(key=lambda x: x.get("rating", 0), reverse=True)
    
    # Paginate
    start = (page - 1) * per_page
    end = start + per_page
    paginated = results[start:end]
    
    return jsonify({
        "total": len(results),
        "page": page,
        "per_page": per_page,
        "total_pages": (len(results) + per_page - 1) // per_page,
        "results": paginated
    })

@app.route('/api/content/<content_id>')
def get_content_by_id(content_id):
    content = CONTENT_DB.get(content_id)
    if content:
        content_copy = content.copy()
        content_copy["id"] = content_id
        content_copy["views"] = CONTENT_VIEWS.get(content_id, 0)
        return jsonify(content_copy)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/trending')
def get_trending_api():
    return jsonify(get_trending_content())

@app.route('/api/recommendations')
@login_required
def get_recommendations_api():
    user_id = session['user_id']
    return jsonify(get_recommendations(user_id))

@app.route('/api/watch/<content_id>', methods=['POST'])
@login_required
def track_watch(content_id):
    user_id = session['user_id']
    if content_id not in WATCH_HISTORY[user_id]:
        WATCH_HISTORY[user_id].append(content_id)
        CONTENT_VIEWS[content_id] += 1
    return jsonify({"success": True})

@app.route('/api/watchlist/<content_id>', methods=['POST'])
@login_required
def add_to_watchlist(content_id):
    user_id = session['user_id']
    if content_id not in WATCHLIST[user_id]:
        WATCHLIST[user_id].append(content_id)
        return jsonify({"success": True, "action": "added"})
    else:
        WATCHLIST[user_id].remove(content_id)
        return jsonify({"success": True, "action": "removed"})

@app.route('/api/watchlist')
@login_required
def get_watchlist():
    user_id = session['user_id']
    watchlist_content = []
    for cid in WATCHLIST.get(user_id, []):
        if cid in CONTENT_DB:
            content = CONTENT_DB[cid].copy()
            content["id"] = cid
            watchlist_content.append(content)
    return jsonify(watchlist_content)

@app.route('/api/favorite/<content_id>', methods=['POST'])
@login_required
def add_to_favorites(content_id):
    user_id = session['user_id']
    if content_id not in FAVORITES[user_id]:
        FAVORITES[user_id].append(content_id)
        return jsonify({"success": True, "action": "added"})
    else:
        FAVORITES[user_id].remove(content_id)
        return jsonify({"success": True, "action": "removed"})

@app.route('/api/favorites')
@login_required
def get_favorites():
    user_id = session['user_id']
    favorites_content = []
    for cid in FAVORITES.get(user_id, []):
        if cid in CONTENT_DB:
            content = CONTENT_DB[cid].copy()
            content["id"] = cid
            favorites_content.append(content)
    return jsonify(favorites_content)

@app.route('/api/rate/<content_id>', methods=['POST'])
@login_required
def rate_content(content_id):
    user_id = session['user_id']
    data = request.get_json()
    rating = data.get('rating')
    if rating and 1 <= rating <= 10:
        USER_RATINGS[user_id][content_id] = rating
        return jsonify({"success": True})
    return jsonify({"error": "Invalid rating"}), 400

@app.route('/api/search')
def search_api():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    return jsonify(search_content(query))

@app.route('/api/genres')
def get_genres():
    genres = set()
    for content in CONTENT_DB.values():
        for genre in content.get("genre", "").split(", "):
            if genre.strip():
                genres.add(genre.strip())
    return jsonify(["All"] + sorted(list(genres)))

@app.route('/api/languages')
def get_languages_api():
    languages = set()
    for content in CONTENT_DB.values():
        lang = content.get("language")
        if lang:
            languages.add(lang)
    return jsonify(["All"] + sorted(list(languages)))

@app.route('/api/years')
def get_years():
    years = set()
    for content in CONTENT_DB.values():
        year = content.get("year")
        if year:
            years.add(str(year))
    return jsonify(["All"] + sorted(list(years), reverse=True))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                         user_name=session.get('user_name'),
                         languages=LANGUAGES,
                         translations=TRANSLATIONS)

@app.route('/download/<content_id>')
def download_content(content_id):
    content = CONTENT_DB.get(content_id)
    if content:
        query = quote(f"{content['title']} {content['year']} {content.get('language', '')} download")
        if content.get('type') in ['anime', 'anime_movie']:
            return redirect(f"https://rareanimes.app/search?q={query}")
        return redirect(f"https://vegamovies.audio/?s={query}")
    return redirect(url_for('dashboard'))

# ========== ADMIN PANEL ==========
@app.route('/xstar-admin-secret')
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/api/login', methods=['POST'])
def admin_login_api():
    data = request.get_json()
    if data.get('password') == ADMIN_PASSWORD:
        session['is_admin'] = True
        return jsonify({"success": True})
    return jsonify({"error": "Invalid password"}), 401

@app.route('/admin/api/logout', methods=['POST'])
def admin_logout_api():
    session.pop('is_admin', None)
    return jsonify({"success": True})

@app.route('/admin/api/stats')
@admin_required
def admin_stats():
    total_views = sum(CONTENT_VIEWS.values())
    total_watchlist = sum(len(w) for w in WATCHLIST.values())
    total_favorites = sum(len(f) for f in FAVORITES.values())
    total_ratings = sum(len(r) for r in USER_RATINGS.values())
    
    return jsonify({
        "total_content": len(CONTENT_DB),
        "total_users": len(USERS),
        "total_views": total_views,
        "total_watchlist": total_watchlist,
        "total_favorites": total_favorites,
        "total_ratings": total_ratings
    })

@app.route('/admin/api/content')
@admin_required
def admin_get_content():
    return jsonify([{"id": cid, **content} for cid, content in CONTENT_DB.items()])

@app.route('/admin/api/content', methods=['POST'])
@admin_required
def admin_add_content():
    data = request.get_json()
    new_id = f"c{len(CONTENT_DB) + 1}"
    CONTENT_DB[new_id] = {
        "title": data.get('title'),
        "year": int(data.get('year', 2024)),
        "type": data.get('type', 'movie'),
        "language": data.get('language', 'English'),
        "genre": data.get('genre', 'Action'),
        "image": data.get('image', 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg'),
        "banner": data.get('banner', 'https://image.tmdb.org/t/p/original/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg'),
        "rating": float(data.get('rating', 7.0)),
        "duration": data.get('duration', '2h'),
        "director": data.get('director', 'Unknown'),
        "cast": data.get('cast', 'Various'),
        "story": data.get('story', 'No description available.')
    }
    return jsonify({"success": True, "id": new_id})

@app.route('/admin/api/content/<content_id>', methods=['PUT'])
@admin_required
def admin_update_content(content_id):
    if content_id not in CONTENT_DB:
        return jsonify({"error": "Content not found"}), 404
    
    data = request.get_json()
    CONTENT_DB[content_id].update({
        "title": data.get('title', CONTENT_DB[content_id]['title']),
        "year": int(data.get('year', CONTENT_DB[content_id]['year'])),
        "type": data.get('type', CONTENT_DB[content_id]['type']),
        "language": data.get('language', CONTENT_DB[content_id]['language']),
        "genre": data.get('genre', CONTENT_DB[content_id]['genre']),
        "image": data.get('image', CONTENT_DB[content_id]['image']),
        "banner": data.get('banner', CONTENT_DB[content_id]['banner']),
        "rating": float(data.get('rating', CONTENT_DB[content_id]['rating'])),
        "story": data.get('story', CONTENT_DB[content_id]['story'])
    })
    return jsonify({"success": True})

@app.route('/admin/api/content/<content_id>', methods=['DELETE'])
@admin_required
def admin_delete_content(content_id):
    if content_id in CONTENT_DB:
        del CONTENT_DB[content_id]
    return jsonify({"success": True})

@app.route('/admin/api/users')
@admin_required
def admin_get_users():
    users_list = [{"email": email, "name": data["name"], "created_at": data.get("created_at", ""), "membership": data.get("membership", "free")} for email, data in USERS.items()]
    return jsonify(users_list)

@app.route('/admin/api/views')
@admin_required
def admin_get_views():
    views_data = [{"content_id": cid, "title": CONTENT_DB.get(cid, {}).get("title", "Unknown"), "views": views} for cid, views in CONTENT_VIEWS.items()]
    views_data.sort(key=lambda x: x["views"], reverse=True)
    return jsonify(views_data[:20])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

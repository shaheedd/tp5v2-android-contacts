plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.example.contacts"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.example.contacts"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            optimization {
                enable = false
            }
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.activity.ktx)
}

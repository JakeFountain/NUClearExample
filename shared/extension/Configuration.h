/*
 * Copyright (C) 2013-2016 Trent Houliston <trent@houliston.me>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
 * Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
 * WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#ifndef EXTENSION_CONFIGURATION_H
#define EXTENSION_CONFIGURATION_H

#include <yaml-cpp/yaml.h>
#include <cstdlib>
#include <nuclear>

#include "FileWatch.h"
#include "utility/support/yaml_expression.h"

namespace extension {

/**
 * TODO document
 *
 * @author Trent Houliston
 */
struct Configuration {
    std::string path;
    YAML::Node config;

    Configuration() : path(""), config(){};
    Configuration(const std::string& path, YAML::Node config) : path(path), config(config){};

    Configuration operator[](const std::string& key) {
        return Configuration(path, config[key]);
    }

    const Configuration operator[](const std::string& key) const {
        return Configuration(path, config[key]);
    }

    Configuration operator[](const char* key) {
        return Configuration(path, config[key]);
    }

    const Configuration operator[](const char* key) const {
        return Configuration(path, config[key]);
    }

    Configuration operator[](size_t index) {
        return Configuration(path, config[index]);
    }

    const Configuration operator[](size_t index) const {
        return Configuration(path, config[index]);
    }

    Configuration operator[](int index) {
        return Configuration(path, config[index]);
    }

    const Configuration operator[](int index) const {
        return Configuration(path, config[index]);
    }

    template <typename T>
    T as() const {
        return config.as<T>();
    }

    // Work for numbers
    template <typename T, std::enable_if_t<std::is_arithmetic<T>::value && !std::is_same<T, char>::value>* = nullptr>
    operator T() const {
        return config.as<utility::support::Expression>();
    }

    template <typename T, std::enable_if_t<std::is_arithmetic<typename T::Scalar>::value>* = nullptr>
    operator T() const {
        return config.as<utility::support::Expression>();
    }

    // Work for strings
    operator std::string() const {
        return config.as<std::string>();
    }
};

}  // namespace extension

// NUClear configuration extension
namespace NUClear {
namespace dsl {
    namespace operation {
        template <>
        struct DSLProxy<::extension::Configuration> {
        private:
            inline static bool endsWith(const std::string& str, const std::string& ending) {
                if (str.length() >= ending.length()) {
                    return (0 == str.compare(str.length() - ending.length(), ending.length(), ending));
                }
                else {
                    return false;
                }
            }

        public:
            template <typename DSL>
            static inline void bind(const std::shared_ptr<threading::Reaction>& reaction, const std::string& path) {
                DSLProxy<::extension::FileWatch>::bind<DSL>(
                    reaction, "config/" + path, ::extension::FileWatch::RENAMED | ::extension::FileWatch::CHANGED);
            }

            template <typename DSL>
            static inline std::shared_ptr<::extension::Configuration> get(threading::Reaction& t) {

                // Get the file watch event
                ::extension::FileWatch watch = DSLProxy<::extension::FileWatch>::get<DSL>(t);

                // Check if the watch is valid
                if (watch && endsWith(watch.path, ".yaml")) {
                    // Return our yaml file
                    try {
                        return std::make_shared<::extension::Configuration>(watch.path, YAML::LoadFile(watch.path));
                    }
                    catch (const YAML::ParserException& e) {
                        throw std::runtime_error(watch.path + " " + std::string(e.what()));
                    }
                }
                else {
                    // Return an empty configuration (which will show up invalid)
                    return std::shared_ptr<::extension::Configuration>(nullptr);
                }
            }
        };
    }  // namespace operation

    // Configuration is transient
    namespace trait {
        template <>
        struct is_transient<std::shared_ptr<::extension::Configuration>> : public std::true_type {};
    }  // namespace trait
}  // namespace dsl
}  // namespace NUClear

#endif  // EXTENSION_CONFIGURATION_H

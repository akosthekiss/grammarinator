// Copyright (c) 2026 Renata Hodovan, Akos Kiss.
//
// Licensed under the BSD 3-Clause License
// <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
// This file may not be copied, modified, or distributed except
// according to those terms.

#ifndef GRAMMARINATOR_UTIL_FMT_HPP
#define GRAMMARINATOR_UTIL_FMT_HPP

#include <array>
#include <charconv>
#include <cstddef>
#include <format>
#include <limits>
#include <span>
#include <string>
#include <string_view>
#include <system_error>
#include <unordered_map>
#include <vector>

namespace grammarinator {
namespace util {

namespace _fmt {

template<class T>
struct named_arg {
  std::string_view name;
  const T& value;
};

struct name_slot {
  std::string_view name;
  bool is_named;
};

template<class T>
constexpr name_slot argument_name(const named_arg<T>& argument) noexcept {
  return {argument.name, true};
}

template<class T>
constexpr name_slot argument_name(const T&) noexcept {
  return {{}, false};
}

template<class T>
constexpr const T& argument_value(named_arg<T>& argument) noexcept {
  return argument.value;
}

template<class T>
constexpr const T& argument_value(const named_arg<T>& argument) noexcept {
  return argument.value;
}

template<class T>
constexpr T& argument_value(T& argument) noexcept {
  return argument;
}

inline bool is_decimal_index(std::string_view text) noexcept {
  if (text.empty()) {
    return false;
  }

  for (const char ch : text) {
    if (ch < '0' || ch > '9') {
      return false;
    }
  }
  return true;
}

inline void validate_names(std::span<const name_slot> names) {
  std::size_t outer_index = 0;
  for (const name_slot slot : names) {
    if (!slot.is_named) {
      ++outer_index;
      continue;
    }

    if (slot.name.empty()) {
      throw std::format_error("format argument names must not be empty");
    }
    if (is_decimal_index(slot.name)) {
      throw std::format_error("a format argument name must not be a decimal index");
    }
    if (slot.name.find_first_of("{}:") != std::string_view::npos) {
      throw std::format_error("a format argument name must not contain '{', '}', or ':'");
    }

    std::size_t inner_index = 0;
    for (const name_slot previous : names) {
      if (inner_index == outer_index) {
        break;
      }
      if (previous.is_named && slot.name == previous.name) {
        throw std::format_error("duplicate format argument name: " + std::string(slot.name));
      }
      ++inner_index;
    }
    ++outer_index;
  }
}

inline void rewrite_id(std::string_view id, std::string& output, std::span<const name_slot> names) {
  // Empty IDs use automatic indexing; decimal IDs are already positional.
  if (id.empty() || is_decimal_index(id)) {
    output.append(id);
    return;
  }

  std::size_t index = 0;
  for (const name_slot slot : names) {
    if (slot.is_named && slot.name == id) {
      char buffer[std::numeric_limits<std::size_t>::digits10 + 2];
      const auto [end, error] = std::to_chars(buffer, buffer + sizeof(buffer), index);

      if (error != std::errc{}) {
        throw std::format_error("format argument index is too large");
      }

      output.append(buffer, end);
      return;
    }
    ++index;
  }

  throw std::format_error("unknown named format argument: " + std::string(id));
}

// Parses and copies one replacement field, including replacement fields nested
// in its format specification (for example "{value:{width}.{precision}f}").
inline void rewrite_field(std::string_view format, std::size_t& position, std::string& output, std::span<const name_slot> names) {
  // The caller has verified format[position] == '{' and that this is not "{{".
  output.push_back('{');
  ++position;

  const std::size_t id_begin = position;
  while (position < format.size() && format[position] != ':' && format[position] != '}' && format[position] != '{') {
    ++position;
  }

  if (position == format.size()) {
    throw std::format_error("unmatched '{' in format string");
  }
  if (format[position] == '{') {
    throw std::format_error("unexpected '{' in format argument name");
  }

  rewrite_id(format.substr(id_begin, position - id_begin), output, names);

  if (format[position] == '}') {
    output.push_back('}');
    ++position;
    return;
  }

  // Copy ':' and parse the format specification until this field's closing
  // brace. A '{' inside the specification begins a nested replacement field.
  output.push_back(':');
  ++position;

  while (position < format.size()) {
    if (format[position] == '{') {
      // Within a format specification, braces introduce dynamic width or
      // precision fields; literal braces are rejected later by vformat.
      rewrite_field(format, position, output, names);
    } else if (format[position] == '}') {
      output.push_back('}');
      ++position;
      return;
    } else {
      output.push_back(format[position]);
      ++position;
    }
  }

  throw std::format_error("unmatched '{' in format string");
}

inline std::string rewrite_format_string(std::string_view format, std::span<const name_slot> names) {
  std::string output;
  output.reserve(format.size());

  std::size_t position = 0;
  while (position < format.size()) {
    if (format[position] == '{') {
      if (position + 1 < format.size() && format[position + 1] == '{') {
        output.append("{{");
        position += 2;
      } else {
        rewrite_field(format, position, output, names);
      }
    } else if (format[position] == '}') {
      if (position + 1 < format.size() && format[position + 1] == '}') {
        output.append("}}");
        position += 2;
      } else {
        throw std::format_error("unmatched '}' in format string");
      }
    } else {
      output.push_back(format[position]);
      ++position;
    }
  }

  return output;
}

} // namespace _fmt

template<class T>
[[nodiscard]] constexpr auto fmtarg(std::string_view name, const T& value) noexcept {
  return _fmt::named_arg<T>{name, value};
}

// Every argument retains its position in the pack. A named argument can be
// referenced either by name or by index; an ordinary argument can be referenced
// by index only. For example:
//
//   fmt("{name}: {1}", fmtarg("name", "answer"), 42)
//
// is rewritten to "{0}: {1}" and formatted with "answer" and 42.
//
// The format string is intentionally a string_view rather than a
// std::format_string<Args...>. A standard format_string would reject named
// fields before this function had an opportunity to rewrite them. Validation of
// the rewritten string is therefore performed at run time by std::vformat.
template<class... Args>
std::string fmt(std::string_view format, Args&&... args) {
  const std::array<_fmt::name_slot, sizeof...(Args)> names{_fmt::argument_name(args)...};
  _fmt::validate_names(names);
  return std::vformat(_fmt::rewrite_format_string(format, names), std::make_format_args(_fmt::argument_value(args)...));
}

inline std::unordered_map<std::string_view, std::string_view> unfmt(std::string_view format, std::string_view text) {
  std::unordered_map<std::string_view, std::string_view> result;

  std::size_t open = format.find('{');

  const std::string_view prefix = open == std::string_view::npos ? format : format.substr(0, open);

  // Stop on an invalid format or a mismatching prefix.
  if (prefix.find('}') != std::string_view::npos || !text.starts_with(prefix)) {
    return result;
  }

  std::size_t text_position = prefix.size();

  // The format contains no placeholders.
  if (open == std::string_view::npos) {
    return result;
  }

  for (;;) {
    // Consecutive placeholders without a literal separator form a group.
    std::vector<std::string_view> group_names;

    std::size_t next_open;
    std::string_view delimiter;

    for (;;) {
      const std::size_t close = format.find('}', open + 1);

      if (close == std::string_view::npos) {
        return result;
      }

      const std::string_view field = format.substr(open + 1, close - open - 1);

      if (field.empty() || field.find('{') != std::string_view::npos) {
        return result;
      }

      const std::size_t colon = field.find(':');
      const std::string_view name = field.substr(0, colon);

      if (name.empty()) {
        return result;
      }

      group_names.push_back(name);

      next_open = format.find('{', close + 1);

      delimiter = next_open == std::string_view::npos ? format.substr(close + 1) : format.substr(close + 1, next_open - close - 1);

      if (delimiter.find('}') != std::string_view::npos) {
        return result;
      }

      // An empty delimiter means that the next placeholder belongs
      // to the same group.
      if (next_open != std::string_view::npos && delimiter.empty()) {
        open = next_open;
        continue;
      }

      break;
    }

    std::size_t value_end;

    if (next_open == std::string_view::npos) {
      // The delimiter after the last placeholder group is the format suffix,
      // so it must occur at the end of the input.
      if (delimiter.size() > text.size() - text_position || !text.ends_with(delimiter)) {
        return result;
      }

      value_end = text.size() - delimiter.size();
    } else {
      value_end = text.find(delimiter, text_position);

      if (value_end == std::string_view::npos) {
        return result;
      }
    }

    // Store the group only after its complete input range has been matched.
    // The first placeholder greedily receives the complete value.
    result.insert_or_assign(group_names.front(), text.substr(text_position, value_end - text_position));

    // Any remaining placeholders in the group receive empty values.
    // Later occurrences of the same name overwrite earlier occurrences.
    for (std::size_t index = 1; index < group_names.size(); ++index) {
      result.insert_or_assign(group_names[index], text.substr(value_end, 0));
    }

    text_position = value_end + delimiter.size();

    if (next_open == std::string_view::npos) {
      return result;
    }

    open = next_open;
  }
}

} // namespace util
} // namespace grammarinator

#endif // GRAMMARINATOR_UTIL_FMT_HPP

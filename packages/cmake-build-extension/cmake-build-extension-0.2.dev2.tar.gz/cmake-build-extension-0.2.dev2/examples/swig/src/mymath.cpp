#include "mymath.h"

#include <algorithm>
#include <stdexcept>
#include <cmath>
#include <functional>
#include <numeric>

double mymath::dot(const std::vector<double>& vector1,
                   const std::vector<double>& vector2)
{
    if (vector1.size() != vector2.size()) {
        throw std::runtime_error("Sizes of the vector do not match");
    }

    double dot = 0;

    for (size_t i = 0; i < vector1.size(); ++i) {
        dot += vector1[i] * vector2[i];
    }

    return dot;
}

std::vector<double> mymath::normalize(const std::vector<double>& input)
{
    auto sumOfSquared = [](double accumulator, const double element) {
        return accumulator + element * element;
    };

    const double norm =
        sqrt(std::accumulate(input.begin(), input.end(), 0.0, sumOfSquared));

    std::vector<double> out;
    out.reserve(input.size());

    std::transform(input.begin(),
                   input.end(),
                   std::back_inserter(out),
                   [&](const double d) -> double { return d / norm; });

    return out;
}
